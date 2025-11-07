"""Global fixtures for virtual_devices integration."""

from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

pytest_plugins = "pytest_homeassistant_custom_component"


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations: None) -> None:
    """Enable custom integrations defined in the test dir."""
    return enable_custom_integrations


@pytest.fixture
def mock_setup_entry() -> Generator[MagicMock]:
    """Mock setting up a config entry."""
    with patch(
        "custom_components.virtual_devices.async_setup_entry", return_value=True
    ):
        yield
