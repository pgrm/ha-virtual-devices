"""Property-based tests for the core logic."""

from hypothesis import given
from hypothesis import strategies as st

from custom_components.virtual_step_dimmer.logic import StepDimmerLogic


@given(
    brightness_steps=st.lists(
        st.integers(min_value=1), min_size=1, max_size=10, unique=True
    ).map(sorted),
    current_power=st.integers(),
    target_brightness=st.integers(),
)
def test_toggles_are_always_within_bounds(
    brightness_steps: list[int], current_power: int, target_brightness: int
) -> None:
    """Test that the number of toggles is always valid."""
    logic = StepDimmerLogic(brightness_steps)
    toggles = logic.get_toggles_for_brightness(current_power, target_brightness)
    assert 0 <= toggles <= logic._num_steps


@given(
    brightness_steps=st.lists(
        st.integers(min_value=1), min_size=1, max_size=10, unique=True
    ).map(sorted),
    power=st.integers(),
)
def test_power_to_step_within_bounds(brightness_steps: list[int], power: int) -> None:
    """Test that power values always map to a valid step."""
    logic = StepDimmerLogic(brightness_steps)
    step = logic._power_to_step(power)
    assert 0 <= step <= logic._num_steps


@given(
    brightness_steps=st.lists(
        st.integers(min_value=1, max_value=10000), min_size=1, max_size=10, unique=True
    ).map(sorted),
    brightness=st.integers(),
)
def test_brightness_to_step_within_bounds(
    brightness_steps: list[int], brightness: int
) -> None:
    """Test that brightness values always map to a valid step."""
    logic = StepDimmerLogic(brightness_steps)
    step = logic._brightness_to_step(brightness)
    assert 0 <= step <= logic._num_steps
