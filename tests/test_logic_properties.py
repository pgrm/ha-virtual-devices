from hypothesis import given
from hypothesis.strategies import integers

from custom_components.virtual_devices.const import LIGHT_BRIGHTNESS_MAX


# Placeholder for the future StepDimmerLogic class
class StepDimmerLogic:
    def __init__(self, initial_brightness: int = 0) -> None:
        self._brightness = initial_brightness

    @property
    def brightness(self) -> int:
        return self._brightness

    def set_brightness(self, value: int) -> None:
        self._brightness = max(0, min(LIGHT_BRIGHTNESS_MAX, value))


@given(
    initial_brightness=integers(min_value=0, max_value=LIGHT_BRIGHTNESS_MAX),
    new_brightness=integers(min_value=0, max_value=LIGHT_BRIGHTNESS_MAX),
)
def test_brightness_is_always_within_bounds(
    initial_brightness: int, new_brightness: int
) -> None:
    """Test that brightness stays within the 0-255 range."""
    logic = StepDimmerLogic(initial_brightness)
    logic.set_brightness(new_brightness)
    assert 0 <= logic.brightness <= LIGHT_BRIGHTNESS_MAX
