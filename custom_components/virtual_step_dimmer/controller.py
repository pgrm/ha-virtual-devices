"""The Step-Dimmer Controller."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

from homeassistant.core import HomeAssistant

from .const import (
    CONF_SETTLING_DELAY_SEC,
    CONF_SWITCH_ENTITY,
    CONF_TOGGLE_DELAY_SEC,
    DEFAULT_SETTLING_DELAY_SEC,
    DEFAULT_TOGGLE_DELAY_SEC,
)
from .logic import StepDimmerLogic


class StepDimmerController:
    """Controls the state and execution of a virtual step dimmer."""

    def __init__(
        self,
        hass: HomeAssistant,
        logic: StepDimmerLogic,
        config: dict[str, Any],
        state_update_callback: Callable[[int, int], None],
    ) -> None:
        """Initialize the controller."""
        self._hass = hass
        self._logic = logic
        self._state_update_callback = state_update_callback

        self._switch_entity_id = config[CONF_SWITCH_ENTITY]
        self._toggle_delay_sec = config.get(
            CONF_TOGGLE_DELAY_SEC, DEFAULT_TOGGLE_DELAY_SEC
        )
        self._settling_delay_sec = config.get(
            CONF_SETTLING_DELAY_SEC, DEFAULT_SETTLING_DELAY_SEC
        )

        self._current_power = 0
        self._pending_brightness: int | None = None
        self._update_task: asyncio.Task | None = None

    def set_target_brightness(self, brightness: int) -> None:
        """Set the desired brightness and trigger an update."""
        self._pending_brightness = brightness
        if self._update_task and not self._update_task.done():
            return
        self._update_task = self._hass.async_create_task(self._execute_update_loop())

    def handle_sensor_update(self, power: float) -> None:
        """Handle a new power reading from the sensor."""
        self._current_power = power
        step = self._logic._power_to_step(power)
        brightness = self._logic._step_to_brightness(step)
        self._state_update_callback(power, brightness)

    async def _execute_update_loop(self) -> None:
        """Execute the update logic in a continuous loop."""
        while self._pending_brightness is not None:
            target_brightness = self._pending_brightness
            self._pending_brightness = None

            toggles = self._logic.get_toggles_for_brightness(
                self._current_power, target_brightness
            )

            for _ in range(toggles):
                await self._hass.services.async_call(
                    "switch",
                    "toggle",
                    {"entity_id": self._switch_entity_id},
                    blocking=True,
                )
                await asyncio.sleep(self._toggle_delay_sec)

            await asyncio.sleep(self._settling_delay_sec)

    def cancel(self) -> None:
        """Cancel any running update task."""
        if self._update_task:
            self._update_task.cancel()
