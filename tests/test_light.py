"""Test the light platform for Virtual Step-Dimmer."""

from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.virtual_step_dimmer.const import (
    CONF_BRIGHTNESS_STEPS,
    CONF_SENSOR_ENTITY,
    CONF_SWITCH_ENTITY,
    DOMAIN,
)


@pytest.fixture
def config_entry_data() -> dict[str, Any]:
    """Return a sample config entry data."""
    return {
        CONF_SWITCH_ENTITY: "switch.test_switch",
        CONF_SENSOR_ENTITY: "sensor.test_sensor",
        CONF_BRIGHTNESS_STEPS: "10, 25, 50, 100",
    }


async def setup_integration(
    hass: HomeAssistant, config_entry_data: dict[str, Any]
) -> MockConfigEntry:
    """Set up the integration."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=config_entry_data)
    config_entry.add_to_hass(hass)
    assert await async_setup_component(hass, DOMAIN, {})
    await hass.async_block_till_done()
    return config_entry


@patch(
    "custom_components.virtual_step_dimmer.light.StepDimmerController",
    autospec=True,
)
@pytest.mark.asyncio
async def test_light_delegates_to_controller(
    mock_controller_class: MagicMock,
    hass: HomeAssistant,
    config_entry_data: dict[str, Any],
) -> None:
    """Test that the light entity correctly delegates calls to the controller."""
    mock_controller = mock_controller_class.return_value
    await setup_integration(hass, config_entry_data)
    entity_id = "light.virtual_step_dimmer"

    await hass.services.async_call(
        "light", "turn_on", {"entity_id": entity_id, "brightness": 128}, blocking=True
    )
    mock_controller.set_target_brightness.assert_called_with(128)

    await hass.services.async_call(
        "light", "turn_off", {"entity_id": entity_id}, blocking=True
    )
    mock_controller.set_target_brightness.assert_called_with(0)


@patch(
    "custom_components.virtual_step_dimmer.light.StepDimmerController",
    autospec=True,
)
@pytest.mark.asyncio
async def test_sensor_and_cancellation(
    mock_controller_class: MagicMock,
    hass: HomeAssistant,
    config_entry_data: dict[str, Any],
) -> None:
    """Test sensor listener and cancellation path."""
    mock_controller = mock_controller_class.return_value
    config_entry = await setup_integration(hass, config_entry_data)

    # Test sensor update
    hass.states.async_set("sensor.test_sensor", "50")
    await hass.async_block_till_done()
    mock_controller.handle_sensor_update.assert_called_with(50.0)

    # Test invalid sensor update
    hass.states.async_set("sensor.test_sensor", "invalid")
    await hass.async_block_till_done()
    # Assert it was not called again
    mock_controller.handle_sensor_update.assert_called_once()

    # Test cancellation
    await hass.config_entries.async_unload(config_entry.entry_id)
    mock_controller.cancel.assert_called_once()
