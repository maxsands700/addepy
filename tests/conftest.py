"""All pytest tests are offline. Live verification is an explicit diagnostics command."""

import os
import socket

import pytest


@pytest.fixture(autouse=True)
def offline_only(monkeypatch):
    # A developer's real environment must never affect mocked contract tests.
    for name in list(os.environ):
        if name.startswith("ADDEPAR_"):
            monkeypatch.delenv(name)
    monkeypatch.setattr("addepy.client.load_dotenv", lambda *args, **kwargs: None)

    def blocked(*args, **kwargs):
        raise AssertionError(
            "Network disabled in offline tests; use python -m addepy.diagnostics for live checks"
        )

    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket.socket, "connect_ex", blocked)
