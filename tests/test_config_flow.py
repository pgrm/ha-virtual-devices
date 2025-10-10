"""Test the config flow for Virtual Devices."""

from unittest.mock import patch

from homeassistant import config_entries, setup
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.virtual_devices.const import (
    CONF_SENSOR_ENTITY,
    CONF_SWITCH_ENTITY,
    DOMAIN,
)


async def _create_config_entry(
    hass: HomeAssistant, switch_entity: str, sensor_entity: str
) -> None:
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
            {
                CONF_SWITCH_ENTITY: switch_entity,
                CONF_SENSOR_ENTITY: sensor_entity,
            },
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Virtual Devices"
    assert result2["data"] == {
        CONF_SWITCH_ENTITY: switch_entity,
        CONF_SENSOR_ENTITY: sensor_entity,
    }
    assert len(mock_setup.mock_calls) == 1


async def test_form_multiple_entries(hass: HomeAssistant, mock_setup_entry) -> None:
    """Test that multiple config entries can be created."""
    await setup.async_setup_component(hass, "persistent_notification", {})
    hass.states.async_set("switch.test_switch", "on")
    hass.states.async_set("sensor.test_sensor", "100")

    # Create the first config entry
    await _create_config_entry(hass, "switch.test_switch", "sensor.test_sensor")

    # Create the second config entry
    hass.states.async_set("switch.test_switch_2", "on")
    hass.states.async_set("sensor.test_sensor_2", "100")
    await _create_config_entry(hass, "switch.test_switch_2", "sensor.test_sensor_2")
