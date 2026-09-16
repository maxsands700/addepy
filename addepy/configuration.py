"""Explicit configuration sources; reading a file never changes the environment."""

import os
from pathlib import Path
from typing import Any, Mapping

from dotenv import dotenv_values


_SETTINGS = {
    "ADDEPAR_FIRM_NAME": "firm_name",
    "ADDEPAR_FIRM_ID": "firm_id",
    "ADDEPAR_ENVIRONMENT": "environment",
    "ADDEPAR_BASE_URL": "base_url",
    "ADDEPAR_API_KEY": "api_key",
    "ADDEPAR_KEY_ID": "key_id",
    "ADDEPAR_KEY_SECRET": "key_secret",
    "ADDEPAR_ACCESS_TOKEN": "access_token",
}
_AUTHENTICATION = {"api_key", "key_id", "key_secret", "access_token", "token_provider"}


def repository_dotenv() -> Path:
    """Select only the nearest Git repository root's .env, starting at cwd."""
    current = Path.cwd()
    for directory in (current, *current.parents):
        marker = directory / ".git"
        # Worktrees and submodules use a .git file instead of a directory.
        if marker.is_dir() or marker.is_file():
            return directory / ".env"
    raise FileNotFoundError(
        "No Git repository found from the current working directory; "
        "pass an explicit file path to AddePy.from_dotenv(...)."
    )


def read_dotenv(path: str | os.PathLike[str]) -> dict[str, str | None]:
    """Read one existing file without interpolation or environment mutation."""
    selected = Path(path)
    if not selected.is_file():
        raise FileNotFoundError(
            f"Credential file does not exist or is not a regular file: {selected}. "
            "Pass an existing file path to AddePy.from_dotenv(...)."
        )
    return dict(dotenv_values(selected, interpolate=False, encoding="utf-8"))


def settings_from_mapping(
    values: Mapping[str, str | None], overrides: Mapping[str, Any]
) -> dict[str, Any]:
    """Map supported variables, replacing authentication as a complete method."""
    settings = {
        argument: values[variable]
        for variable, argument in _SETTINGS.items()
        if variable in values
    }
    if _AUTHENTICATION.intersection(overrides):
        for argument in _AUTHENTICATION:
            settings.pop(argument, None)
    settings.update(overrides)
    return settings
