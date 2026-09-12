"""Shared pytest fixtures for testing custom_components/edenic_bluelab."""

import pytest

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):  # noqa: ARG001
    """Allow Home Assistant to discover custom_components/ during tests."""
    return
