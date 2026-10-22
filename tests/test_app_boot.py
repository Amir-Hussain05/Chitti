"""
tests/test_app_boot.py

Day 1 smoke test: proves the app boots cleanly when config is valid,
and fails fast (no crash, just sys.exit(1)) when required config
(the API key) is missing.
"""

import pytest

from configs.settings import Settings
from core import app as app_module


def test_bootstrap_succeeds_with_valid_config(monkeypatch):
    fake_settings = Settings(ANTHROPIC_API_KEY="fake-key-for-test")
    monkeypatch.setattr(app_module, "settings", fake_settings)

    # Should not raise / should not call sys.exit
    app_module.bootstrap()


def test_bootstrap_fails_fast_without_api_key(monkeypatch):
    fake_settings = Settings(ANTHROPIC_API_KEY="")
    monkeypatch.setattr(app_module, "settings", fake_settings)

    with pytest.raises(SystemExit) as exc_info:
        app_module.bootstrap()

    assert exc_info.value.code == 1
