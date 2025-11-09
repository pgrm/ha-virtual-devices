"""Core logic for the Virtual Step-Dimmer."""

from __future__ import annotations

import logging

from .const import LIGHT_BRIGHTNESS_MAX

_LOGGER = logging.getLogger(__name__)


class StepDimmerLogic:
    """Handles the state machine logic for the step dimmer."""

    def __init__(self, brightness_steps: list[int]) -> None:
        """Initialize the logic handler."""
        if not brightness_steps:
            raise ValueError("Brightness steps cannot be empty")
        self._brightness_steps = sorted(brightness_steps)
        self._num_steps = len(self._brightness_steps)

    def _power_to_step(self, power: float) -> int:
        """Find the closest step for a given power value."""
        if power <= 0:
            return 0
        closest_step_value = min(self._brightness_steps, key=lambda x: abs(x - power))
        return self._brightness_steps.index(closest_step_value) + 1

    def _brightness_to_step(self, brightness: int) -> int:
        """Convert a brightness value (0-255) to a step."""
        brightness = max(0, min(brightness, LIGHT_BRIGHTNESS_MAX))
        return round((brightness / LIGHT_BRIGHTNESS_MAX) * self._num_steps)

    def _step_to_brightness(self, step: int) -> int:
        """Convert a step to a brightness value (0-255)."""
        if step == 0:
            return 0
        return int((step / self._num_steps) * LIGHT_BRIGHTNESS_MAX)

    def get_toggles_for_brightness(
        self, current_power: float, target_brightness: int
    ) -> int:
        """Calculate the number of toggles to reach the target brightness."""
        current_step = self._power_to_step(current_power)
        target_step = self._brightness_to_step(target_brightness)

        _LOGGER.debug("Current Step: %s, Target Step: %s", current_step, target_step)

        if target_step == current_step:
            return 0

        if target_step == 0:
            # Turning off requires one toggle if the light is on.
            return 1 if current_step > 0 else 0

        if current_step == 0:
            # From OFF, it takes (2 * n - 1) toggles to reach step n
            return (target_step * 2) - 1

        # If both on, it takes 2 toggles to move one step
        if target_step > current_step:
            return (target_step - current_step) * 2

        # Cycling through
        return (self._num_steps - current_step + target_step) * 2
