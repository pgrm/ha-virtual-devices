"""Test the light platform for Virtual Devices."""

from unittest.mock import AsyncMock

from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.virtual_devices.const import DOMAIN
from custom_components.virtual_devices.light import async_setup_entry


async def test_setup_entry_no_entities(hass: HomeAssistant):
    """Test that no entities are added."""
    config_entry = MockConfigEntry(domain=DOMAIN, data={})
    async_add_entities = AsyncMock()

    await async_setup_entry(hass, config_entry, async_add_entities)

    async_add_entities.assert_not_called()
