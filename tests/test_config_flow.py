"""Test the config flow for Virtual Step-Dimmer."""

from unittest.mock import patch

import pytest
from homeassistant import config_entries, setup
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.virtual_step_dimmer.const import (
    CONF_BRIGHTNESS_STEPS,
    CONF_SENSOR_ENTITY,
    CONF_SETTLING_DELAY_SEC,
    CONF_SWITCH_ENTITY,
    CONF_TOGGLE_DELAY_SEC,
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

    # Provide switch and sensor entities
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_SWITCH_ENTITY: "switch.test_switch",
            CONF_SENSOR_ENTITY: "sensor.test_sensor",
        },
    )
    assert result2["type"] is FlowResultType.FORM
    assert result2["step_id"] == "brightness"

    # Provide brightness steps
    result3 = await hass.config_entries.flow.async_configure(
        result2["flow_id"], {CONF_BRIGHTNESS_STEPS: "10, 25, 50, 100"}
    )
    assert result3["type"] is FlowResultType.FORM
    assert result3["step_id"] == "advanced"

    # Provide advanced options
    with patch(
        "homeassistant.config_entries.ConfigEntries.async_setup", return_value=True
    ) as mock_setup:
        result4 = await hass.config_entries.flow.async_configure(
            result3["flow_id"],
            {CONF_TOGGLE_DELAY_SEC: 0.6, CONF_SETTLING_DELAY_SEC: 2.1},
        )

    # Check if the entry is created
    assert result4["type"] is FlowResultType.CREATE_ENTRY
    assert result4["data"] == {
        CONF_SWITCH_ENTITY: "switch.test_switch",
        CONF_SENSOR_ENTITY: "sensor.test_sensor",
        CONF_BRIGHTNESS_STEPS: "10, 25, 50, 100",
        CONF_TOGGLE_DELAY_SEC: 0.6,
        CONF_SETTLING_DELAY_SEC: 2.1,
    }
    assert len(mock_setup.mock_calls) == 1


@pytest.mark.asyncio
async def test_brightness_validation_error(hass: HomeAssistant) -> None:
    """Test that an error is shown for invalid brightness steps."""
    # Start the config flow and get to the brightness step
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    result2 = await hass.config_entries.flow.async_configure(
        result["flow_id"],
        {
            CONF_SWITCH_ENTITY: "switch.test_switch",
            CONF_SENSOR_ENTITY: "sensor.test_sensor",
        },
    )

    # Provide invalid brightness steps
    result3 = await hass.config_entries.flow.async_configure(
        result2["flow_id"], {CONF_BRIGHTNESS_STEPS: "10, abc, 50"}
    )

    assert result3["type"] is FlowResultType.FORM
    assert result3["errors"]["base"] == "invalid_brightness_steps"
