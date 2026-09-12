"""Shared pytest fixtures for testing custom_components/edenic_bluelab."""

import pathlib

import pytest
import yaml

SECRETS_PATH = pathlib.Path(__file__).parent / "secrets.yaml"
REQUIRED_SECRET_KEYS = {"org_key", "api_key", "device_label"}


@pytest.fixture(scope="session")
def edenic_credentials():
    """
    Real Edenic credentials for live API tests, loaded from tests_live/secrets.yaml.

    Skips the test if the file is missing or incomplete, so `pytest -m live`
    fails loudly with a clear message rather than a stack trace.
    """
    if not SECRETS_PATH.exists():
        pytest.skip(
            "tests_live/secrets.yaml not found. Copy tests_live/secrets.yaml.template to "
            "tests_live/secrets.yaml and fill in real Edenic credentials to run live "
            "API tests."
        )
    data = yaml.safe_load(SECRETS_PATH.read_text(encoding="utf-8")) or {}
    missing = REQUIRED_SECRET_KEYS - data.keys()
    if missing:
        pytest.skip(f"tests_live/secrets.yaml is missing keys: {', '.join(missing)}")
    return data
