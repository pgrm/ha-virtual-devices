"""Test the config flow for Virtual Devices."""

from unittest.mock import MagicMock, patch

from homeassistant import config_entries, setup
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.virtual_devices.const import DOMAIN


async def _create_config_entry(hass: HomeAssistant) -> None:
    """Create a config entry for a virtual device."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] is None

    with patch(
        "homeassistant.config_entries.ConfigEntries.async_setup",
        return_value=True,
    ) as mock_setup:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Virtual Devices"
    assert result2["data"] == {}
    assert len(mock_setup.mock_calls) == 1


async def test_form_multiple_entries(
    hass: HomeAssistant, mock_setup_entry: MagicMock
) -> None:
    """Test that multiple config entries can be created."""
    await setup.async_setup_component(hass, "persistent_notification", {})

    # Create the first config entry
    await _create_config_entry(hass)

    # Create the second config entry
    await _create_config_entry(hass)
