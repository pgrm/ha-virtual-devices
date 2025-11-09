"""Test the light platform for Virtual Step-Dimmer."""

from typing import Any

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


@pytest.mark.asyncio
async def test_light_entity_setup(
    hass: HomeAssistant, config_entry_data: dict[str, Any]
) -> None:
    """Test the setup of the light entity."""
    await setup_integration(hass, config_entry_data)
    entity_id = "light.virtual_step_dimmer"
    state = hass.states.get(entity_id)
    assert state is not None
    assert state.name == "Virtual Step-Dimmer"


@pytest.mark.asyncio
async def test_turn_on(
    hass: HomeAssistant,
    config_entry_data: dict[str, Any],
    service_calls,
) -> None:
    """Test turning the light on."""
    await setup_integration(hass, config_entry_data)
    entity_id = "light.virtual_step_dimmer"

    # Manually set the current power for the test
    hass.states.async_set("sensor.test_sensor", "10")
    await hass.async_block_till_done()

    # Target brightness for step 3 (50W)
    await hass.services.async_call(
        "light",
        "turn_on",
        {"entity_id": entity_id, "brightness": 191},
        blocking=True,
    )
    await hass.async_block_till_done()

    switch_calls = [call for call in service_calls if call.domain == "switch"]
    # From step 1 to step 3 needs 2 toggles
    assert len(switch_calls) == 2
    assert switch_calls[0].service == "toggle"


@pytest.mark.asyncio
async def test_turn_off(
    hass: HomeAssistant,
    config_entry_data: dict[str, Any],
    service_calls,
) -> None:
    """Test turning the light off."""
    await setup_integration(hass, config_entry_data)
    entity_id = "light.virtual_step_dimmer"

    await hass.services.async_call(
        "light", "turn_off", {"entity_id": entity_id}, blocking=True
    )
    await hass.async_block_till_done()

    switch_calls = [call for call in service_calls if call.domain == "switch"]
    assert len(switch_calls) == 1
    assert switch_calls[0].service == "turn_off"
