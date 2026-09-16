"""Configuration source isolation, credential precedence, and repository discovery."""

import base64
import os
from unittest.mock import Mock

import pytest
import requests

from addepy import AddePy


SETTINGS = {
    "ADDEPAR_FIRM_NAME": "filefirm",
    "ADDEPAR_FIRM_ID": "123",
    "ADDEPAR_ENVIRONMENT": "sandbox",
    "ADDEPAR_API_KEY": "file-key",
}


def write_env(path, values=None):
    values = SETTINGS if values is None else values
    path.write_text(
        "".join(f"{key}={value}\n" for key, value in values.items()), encoding="utf-8"
    )
    return path


def set_env(monkeypatch, values):
    for key, value in values.items():
        monkeypatch.setenv(key, value)


@pytest.fixture
def session():
    result = requests.Response()
    result.status_code = 200
    result._content = b'{"data": []}'
    fake = Mock(spec=requests.Session)
    fake.request.return_value = result
    return fake


def headers(client, session):
    client.request("GET", "/entities")
    return session.request.call_args.kwargs["headers"]


def from_source(source, values, tmp_path, monkeypatch, **overrides):
    if source == "environment":
        set_env(monkeypatch, values)
        return AddePy.from_env(**overrides)
    return AddePy.from_dotenv(
        write_env(tmp_path / "credentials.env", values), **overrides
    )


def test_constructor_ignores_environment_and_dotenv(tmp_path, monkeypatch, session):
    (tmp_path / ".git").mkdir()
    write_env(tmp_path / ".env")
    monkeypatch.chdir(tmp_path)
    set_env(monkeypatch, SETTINGS)
    monkeypatch.setenv("ADDEPAR_BASE_URL", "https://ambient.sandbox.addepar.com/api/v1")

    with AddePy("explicit", "456", "explicit-key", session=session) as client:
        assert client.base_url == "https://explicit.addepar.com/api/v1"
        sent = headers(client, session)
        assert sent["Addepar-Firm"] == "456"
        assert sent["Authorization"] == "Basic explicit-key"
    session.close.assert_not_called()


@pytest.mark.parametrize("missing", ["firm_name", "firm_id", "api_key"])
def test_constructor_cannot_fill_missing_settings_from_environment(
    missing, monkeypatch
):
    set_env(monkeypatch, SETTINGS)
    arguments = {"firm_name": "explicit", "firm_id": "456", "api_key": "explicit-key"}
    arguments.pop(missing)
    with pytest.raises(ValueError):
        AddePy(**arguments)


@pytest.mark.parametrize("source", ["environment", "dotenv"])
@pytest.mark.parametrize(
    "auth,expected",
    [
        ({"ADDEPAR_API_KEY": "encoded"}, "Basic encoded"),
        ({"ADDEPAR_ACCESS_TOKEN": "token"}, "Bearer token"),
        (
            {"ADDEPAR_KEY_ID": "key", "ADDEPAR_KEY_SECRET": "secret"},
            "Basic " + base64.b64encode(b"key:secret").decode(),
        ),
    ],
)
def test_factories_support_authentication_methods(
    source, auth, expected, tmp_path, monkeypatch, session
):
    values = {key: value for key, value in SETTINGS.items() if key != "ADDEPAR_API_KEY"}
    values.update(auth)
    with from_source(source, values, tmp_path, monkeypatch, session=session) as client:
        assert client.base_url == "https://filefirm.sandbox.addepar.com/api/v1"
        sent = headers(client, session)
        assert sent["Authorization"] == expected
        assert sent["Addepar-Firm"] == "123"


def test_from_env_never_reads_dotenv(tmp_path, monkeypatch, session):
    (tmp_path / ".git").mkdir()
    write_env(tmp_path / ".env")
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError):
        AddePy.from_env()
    set_env(monkeypatch, {**SETTINGS, "ADDEPAR_API_KEY": "environment-key"})
    with AddePy.from_env(session=session) as client:
        assert headers(client, session)["Authorization"] == "Basic environment-key"


@pytest.mark.parametrize(
    "missing", ["ADDEPAR_FIRM_NAME", "ADDEPAR_FIRM_ID", "ADDEPAR_API_KEY"]
)
def test_dotenv_never_fills_missing_values_from_environment(
    missing, tmp_path, monkeypatch
):
    set_env(monkeypatch, SETTINGS)
    incomplete = {key: value for key, value in SETTINGS.items() if key != missing}
    path = write_env(tmp_path / ".env", incomplete)
    with pytest.raises(ValueError):
        AddePy.from_dotenv(path)


def test_dotenv_does_not_interpolate_or_mutate_environment(
    tmp_path, monkeypatch, session
):
    set_env(monkeypatch, {**SETTINGS, "ADDEPAR_API_KEY": "ambient-key"})
    monkeypatch.setenv("PRIVATE_TOKEN", "ambient-secret")
    path = write_env(
        tmp_path / ".env",
        {
            **SETTINGS,
            "ADDEPAR_API_KEY": "${PRIVATE_TOKEN}",
            "PRIVATE_TOKEN": "file-secret",
        },
    )
    before = dict(os.environ)
    with AddePy.from_dotenv(path, session=session) as client:
        assert headers(client, session)["Authorization"] == "Basic ${PRIVATE_TOKEN}"
    assert dict(os.environ) == before


@pytest.mark.parametrize("source", ["environment", "dotenv"])
def test_explicit_arguments_override_source(source, tmp_path, monkeypatch, session):
    values = {
        **SETTINGS,
        "ADDEPAR_BASE_URL": "https://source.sandbox.addepar.com/api/v1",
    }
    before = dict(values)
    with from_source(
        source,
        values,
        tmp_path,
        monkeypatch,
        firm_id="456",
        base_url="https://explicit.clientdev.addepar.com/api/v1",
        environment="development",
        session=session,
    ) as client:
        assert client.base_url == "https://explicit.clientdev.addepar.com/api/v1"
        assert client.environment == "development"
        sent = headers(client, session)
        assert sent["Addepar-Firm"] == "456"
        assert sent["Authorization"] == "Basic file-key"
    assert values == before


@pytest.mark.parametrize("source", ["environment", "dotenv"])
@pytest.mark.parametrize(
    "override,expected",
    [
        ({"access_token": "explicit-token"}, "Bearer explicit-token"),
        ({"api_key": "explicit-key"}, "Basic explicit-key"),
        (
            {"key_id": "new-id", "key_secret": "new-secret"},
            "Basic " + base64.b64encode(b"new-id:new-secret").decode(),
        ),
        ({"token_provider": lambda: "refreshed"}, "Bearer refreshed"),
    ],
)
def test_explicit_authentication_replaces_entire_source_method(
    source, override, expected, tmp_path, monkeypatch, session
):
    # Even conflicting source credentials are superseded by an explicit method.
    values = {
        **SETTINGS,
        "ADDEPAR_ACCESS_TOKEN": "old-token",
        "ADDEPAR_KEY_SECRET": "old-secret",
    }
    with from_source(
        source, values, tmp_path, monkeypatch, session=session, **override
    ) as client:
        assert headers(client, session)["Authorization"] == expected


@pytest.mark.parametrize("source", ["environment", "dotenv"])
@pytest.mark.parametrize(
    "override", [{"key_id": "new-id"}, {"key_secret": "new-secret"}]
)
def test_key_pair_cannot_mix_explicit_and_source_credentials(
    source, override, tmp_path, monkeypatch
):
    values = {
        **SETTINGS,
        "ADDEPAR_KEY_ID": "old-id",
        "ADDEPAR_KEY_SECRET": "old-secret",
    }
    with pytest.raises(ValueError, match="supplied together"):
        from_source(source, values, tmp_path, monkeypatch, **override)


@pytest.mark.parametrize("source", ["environment", "dotenv"])
def test_explicit_none_clears_source_authentication(source, tmp_path, monkeypatch):
    with pytest.raises(ValueError, match="exactly one authentication method"):
        from_source(source, SETTINGS, tmp_path, monkeypatch, api_key=None)


@pytest.mark.parametrize("source", ["environment", "dotenv"])
@pytest.mark.parametrize(
    "auth",
    [
        {"ADDEPAR_API_KEY": "encoded", "ADDEPAR_ACCESS_TOKEN": "token"},
        {"ADDEPAR_KEY_ID": "key"},
        {"ADDEPAR_KEY_ID": "", "ADDEPAR_KEY_SECRET": "secret"},
        {"ADDEPAR_KEY_ID": "key", "ADDEPAR_KEY_SECRET": ""},
        {"ADDEPAR_API_KEY": ""},
    ],
)
def test_invalid_source_authentication_is_rejected(source, auth, tmp_path, monkeypatch):
    values = {key: value for key, value in SETTINGS.items() if key != "ADDEPAR_API_KEY"}
    with pytest.raises(ValueError):
        from_source(source, {**values, **auth}, tmp_path, monkeypatch)


@pytest.mark.parametrize("git_marker", ["directory", "file"])
def test_discovery_uses_nearest_repository_root_only(
    git_marker, tmp_path, monkeypatch, session
):
    (tmp_path / ".git").mkdir()
    write_env(tmp_path / ".env", {**SETTINGS, "ADDEPAR_API_KEY": "outer-key"})
    repository = tmp_path / "nested-repository"
    repository.mkdir()
    marker = repository / ".git"
    if git_marker == "directory":
        marker.mkdir()
    else:
        marker.write_text("gitdir: ../worktree-metadata\n")
    write_env(repository / ".env")
    child = repository / "scripts" / "nested"
    child.mkdir(parents=True)
    write_env(child / ".env", {**SETTINGS, "ADDEPAR_API_KEY": "child-key"})
    monkeypatch.chdir(child)
    with AddePy.from_dotenv(session=session) as client:
        assert headers(client, session)["Authorization"] == "Basic file-key"


def test_missing_root_env_does_not_search_beyond_repository_or_use_nested_env(
    tmp_path, monkeypatch
):
    (tmp_path / ".git").mkdir()
    write_env(tmp_path / ".env")
    repository = tmp_path / "inner"
    repository.mkdir()
    (repository / ".git").write_text("gitdir: ../metadata\n")
    child = repository / "scripts"
    child.mkdir()
    write_env(child / ".env")
    monkeypatch.chdir(child)
    with pytest.raises(FileNotFoundError, match="inner/.env"):
        AddePy.from_dotenv()


def test_discovery_requires_repository_even_when_cwd_has_env(tmp_path, monkeypatch):
    write_env(tmp_path / ".env")
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError, match="No Git repository"):
        AddePy.from_dotenv()


@pytest.mark.parametrize("absolute", [False, True])
def test_explicit_path_works_outside_git_repository(
    absolute, tmp_path, monkeypatch, session
):
    write_env(tmp_path / ".env", {**SETTINGS, "ADDEPAR_API_KEY": "wrong-key"})
    chosen = write_env(tmp_path / ".env.sandbox")
    monkeypatch.chdir(tmp_path)
    path = chosen if absolute else ".env.sandbox"
    with AddePy.from_dotenv(path, session=session) as client:
        assert headers(client, session)["Authorization"] == "Basic file-key"


@pytest.mark.parametrize("directory", [False, True])
def test_explicit_file_must_exist_and_be_a_regular_file(
    directory, tmp_path, monkeypatch
):
    set_env(monkeypatch, SETTINGS)
    selected = tmp_path / "credentials"
    if directory:
        selected.mkdir()
    with pytest.raises(FileNotFoundError, match="Credential file"):
        AddePy.from_dotenv(selected)


def test_dotenv_default_environment_is_independent_of_process(
    tmp_path, monkeypatch, session
):
    monkeypatch.setenv("ADDEPAR_ENVIRONMENT", "sandbox")
    values = {
        key: value for key, value in SETTINGS.items() if key != "ADDEPAR_ENVIRONMENT"
    }
    with AddePy.from_dotenv(
        write_env(tmp_path / ".env", values), session=session
    ) as client:
        assert client.base_url == "https://filefirm.addepar.com/api/v1"


def test_factories_preserve_subclasses(tmp_path, monkeypatch, session):
    class CustomClient(AddePy):
        pass

    set_env(monkeypatch, SETTINGS)
    with CustomClient.from_env(session=session) as client:
        assert isinstance(client, CustomClient)
    with CustomClient.from_dotenv(
        write_env(tmp_path / ".env"), session=session
    ) as client:
        assert isinstance(client, CustomClient)
