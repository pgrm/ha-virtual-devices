from hypothesis import given
from hypothesis.strategies import integers


# Placeholder for the future StepDimmerLogic class
class StepDimmerLogic:
    def __init__(self, initial_brightness=0):
        self._brightness = initial_brightness

    @property
    def brightness(self):
        return self._brightness

    def set_brightness(self, value):
        self._brightness = max(0, min(255, value))


@given(
    initial_brightness=integers(min_value=0, max_value=255),
    new_brightness=integers(min_value=0, max_value=255),
)
def test_brightness_is_always_within_bounds(initial_brightness, new_brightness):
    """Test that brightness stays within the 0-255 range."""
    logic = StepDimmerLogic(initial_brightness)
    logic.set_brightness(new_brightness)
    assert 0 <= logic.brightness <= 255
