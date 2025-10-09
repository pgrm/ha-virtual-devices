"""Test the initial setup of the integration."""

from unittest.mock import AsyncMock, patch

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.virtual_devices import (
    PLATFORMS,
    async_setup_entry,
    async_unload_entry,
)
from custom_components.virtual_devices.const import DOMAIN


async def test_setup_and_unload_entry(hass: HomeAssistant):
    """Test that the integration can be set up and unloaded."""
    entry = MockConfigEntry(domain=DOMAIN, data={}, entry_id="test")

    with patch.object(
        hass.config_entries,
        "async_setup_platforms",
        new_callable=AsyncMock,
        return_value=True,
        create=True,
    ) as mock_setup_platforms:
        assert await async_setup_entry(hass, entry) is True
        mock_setup_platforms.assert_called_once_with(entry, PLATFORMS)

    with patch.object(
        hass.config_entries,
        "async_unload_platforms",
        new_callable=AsyncMock,
        return_value=True,
    ) as mock_unload_platforms:
        assert await async_unload_entry(hass, entry) is True
        mock_unload_platforms.assert_called_once_with(entry, PLATFORMS)
