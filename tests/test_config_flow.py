"""Test the config flow for Virtual Step-Dimmer."""

from unittest.mock import patch

import pytest
from homeassistant import config_entries, setup
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.virtual_step_dimmer.const import (
    CONF_BRIGHTNESS_STEPS,
    CONF_SENSOR_ENTITY,
    CONF_SWITCH_ENTITY,
    DOMAIN,
)


@pytest.mark.asyncio
async def test_full_config_flow(hass: HomeAssistant) -> None:
    """Test the full config flow from user step to brightness step."""
    await setup.async_setup_component(hass, "persistent_notification", {})
    hass.states.async_set("switch.test_switch", "on")
    hass.states.async_set("sensor.test_sensor", "100")

    # Start the config flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] is None

    # Provide switch and sensor entities
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_SWITCH_ENTITY: "switch.test_switch",
            CONF_SENSOR_ENTITY: "sensor.test_sensor",
        },
    )
    await hass.async_block_till_done()

    # Check if it moved to the brightness step
    assert result2["type"] is FlowResultType.FORM
    assert result2["step_id"] == "brightness"
    assert not result2["errors"]

    # Provide brightness steps
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_setup",
        return_value=True,
    ) as mock_setup:
        result3 = await hass.config_entries.flow.async_configure(
            result2["flow_id"],
            {
                CONF_BRIGHTNESS_STEPS: "10, 25, 50, 100",
            },
        )
        await hass.async_block_till_done()

    # Check if the entry is created
    assert result3["type"] is FlowResultType.CREATE_ENTRY
    assert result3["title"] == "Virtual Step-Dimmer"
    assert result3["data"] == {
        CONF_SWITCH_ENTITY: "switch.test_switch",
        CONF_SENSOR_ENTITY: "sensor.test_sensor",
        CONF_BRIGHTNESS_STEPS: "10, 25, 50, 100",
    }
    assert len(mock_setup.mock_calls) == 1
