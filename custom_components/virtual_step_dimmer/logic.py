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

    def get_toggles_for_brightness(
        self, current_power: float, target_brightness: int
    ) -> int:
        """
        Calculate the number of toggles to reach the target brightness.

        Returns:
            The number of toggles required.
        """
        current_step = self._power_to_step(current_power)
        target_step = self._brightness_to_step(target_brightness)

        _LOGGER.debug("Current Step: %s, Target Step: %s", current_step, target_step)

        if target_step == current_step:
            return 0

        # The number of toggles is the difference in steps.
        # The dimmer cycles through steps, so we can calculate the delta.
        if target_step > current_step:
            return target_step - current_step
        else:
            # Cycle through the remaining steps and back to the target
            return self._num_steps - current_step + target_step
