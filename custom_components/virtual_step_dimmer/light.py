"""Platform for light integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.light import ATTR_BRIGHTNESS, ColorMode, LightEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_BRIGHTNESS_STEPS,
    CONF_SENSOR_ENTITY,
    DOMAIN,
    LIGHT_BRIGHTNESS_MAX,
)
from .controller import StepDimmerController
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
        self.config_entry = config_entry
        self._attr_name = "Virtual Step-Dimmer"
        self._attr_unique_id = config_entry.entry_id
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        self._attr_color_mode = ColorMode.BRIGHTNESS

        self._current_brightness = 0
        self._current_power = 0

        brightness_steps = [
            int(s.strip()) for s in config_entry.data[CONF_BRIGHTNESS_STEPS].split(",")
        ]
        logic = StepDimmerLogic(brightness_steps)

        self._controller = StepDimmerController(
            hass,
            logic,
            config_entry.data,
            self._on_state_update,
        )

    @callback
    def _on_state_update(self, power: float, brightness: int) -> None:
        """Receive state updates from the controller."""
        self._current_power = power
        self._current_brightness = brightness
        self.async_write_ha_state()

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
        brightness = kwargs.get(ATTR_BRIGHTNESS, LIGHT_BRIGHTNESS_MAX)
        self._controller.set_target_brightness(brightness)

    async def async_turn_off(self, **kwargs: dict[str, Any]) -> None:
        """Turn the light off."""
        self._controller.set_target_brightness(0)

    async def async_will_remove_from_hass(self) -> None:
        """Cancel the controller's task when the entity is removed."""
        self._controller.cancel()

    async def async_added_to_hass(self) -> None:
        """Register callbacks."""

        @callback
        def sensor_state_listener(event: Event) -> None:
            """Handle sensor state changes."""
            new_state = event.data.get("new_state")
            if new_state is None or new_state.state in ("unknown", "unavailable"):
                return

            try:
                power = float(new_state.state)
                self._controller.handle_sensor_update(power)
            except (ValueError, TypeError):
                _LOGGER.warning("Could not parse sensor value: %s", new_state.state)

        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self.config_entry.data[CONF_SENSOR_ENTITY]],
                sensor_state_listener,
            )
        )
