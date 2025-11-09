"""Platform for light integration."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ColorMode,
    LightEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_BRIGHTNESS_STEPS,
    CONF_SENSOR_ENTITY,
    CONF_SWITCH_ENTITY,
    DOMAIN,
    LIGHT_BRIGHTNESS_MAX,
)
from .logic import StepDimmerLogic

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the light platform for Virtual Step-Dimmer."""
    async_add_entities([VirtualStepDimmerLight(hass, config_entry)])


class VirtualStepDimmerLight(LightEntity):
    """Representation of a Virtual Step-Dimmer Light."""

    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the light."""
        self.hass = hass
        self.config_entry = config_entry
        self._switch_entity = self.config_entry.data[CONF_SWITCH_ENTITY]
        self._sensor_entity = self.config_entry.data[CONF_SENSOR_ENTITY]
        self._brightness_steps_str = self.config_entry.data[CONF_BRIGHTNESS_STEPS]

        brightness_steps = [
            int(s.strip()) for s in self._brightness_steps_str.split(",")
        ]
        self._logic = StepDimmerLogic(brightness_steps)

        self._attr_name = "Virtual Step-Dimmer"
        self._attr_unique_id = config_entry.entry_id
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        self._attr_color_mode = ColorMode.BRIGHTNESS

        self._current_brightness = 0
        self._current_power = 0

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=self.name,
            manufacturer="Virtual Devices",
        )

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self._current_brightness > 0

    @property
    def brightness(self) -> int:
        """Return the brightness of the light."""
        return self._current_brightness

    async def async_turn_on(self, **kwargs: dict[str, Any]) -> None:
        """Turn the light on."""
        target_brightness = kwargs.get(ATTR_BRIGHTNESS, LIGHT_BRIGHTNESS_MAX)

        toggles = self._logic.get_toggles_for_brightness(
            self._current_power, target_brightness
        )

        _LOGGER.debug(
            "Turning on with target brightness: %s. Toggles needed: %s",
            target_brightness,
            toggles,
        )

        for i in range(toggles):
            _LOGGER.debug("Toggling switch, iteration %s", i + 1)
            await self.hass.services.async_call(
                "switch",
                "toggle",
                {"entity_id": self._switch_entity},
                blocking=True,
            )
            # Add a small delay between toggles to allow the physical device to respond
            await asyncio.sleep(0.5)

        # We don't set the brightness here, we wait for the sensor to update
        # and the state listener will update the brightness.

    async def async_turn_off(self, **kwargs: dict[str, Any]) -> None:
        """Turn the light off."""
        _LOGGER.debug("Turning off")
        await self.hass.services.async_call(
            "switch",
            "turn_off",
            {"entity_id": self._switch_entity},
            blocking=True,
        )
        self._current_brightness = 0
        self.async_write_ha_state()

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""

        @callback
        def sensor_state_listener(event: Event) -> None:
            """Handle sensor state changes."""
            new_state = event.data.get("new_state")
            if new_state is None:
                return

            try:
                power = float(new_state.state)
                self._current_power = power
                step = self._logic._power_to_step(power)
                if step == 0:
                    self._current_brightness = 0
                else:
                    self._current_brightness = int(
                        (step / self._logic._num_steps) * LIGHT_BRIGHTNESS_MAX
                    )
            except (ValueError, TypeError):
                self._current_brightness = 0

            self.async_write_ha_state()

        self.async_on_remove(
            async_track_state_change_event(
                self.hass, [self._sensor_entity], sensor_state_listener
            )
        )
