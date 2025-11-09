"""Test the core logic for the Virtual Step-Dimmer."""

import pytest

from custom_components.virtual_step_dimmer.logic import StepDimmerLogic


@pytest.fixture
def brightness_steps() -> list[int]:
    """Return a sample list of brightness steps."""
    return [10, 25, 50, 100]


def test_initialization(brightness_steps: list[int]) -> None:
    """Test the initialization of the StepDimmerLogic."""
    logic = StepDimmerLogic(brightness_steps)
    assert logic._brightness_steps == [10, 25, 50, 100]
    assert logic._num_steps == 4

    with pytest.raises(ValueError):
        StepDimmerLogic([])


@pytest.mark.parametrize(
    "power, expected_step",
    [
        (0, 0),
        (5, 1),
        (10, 1),
        (18, 2),
        (25, 2),
        (70, 3),
        (110, 4),
    ],
)
def test_power_to_step(
    brightness_steps: list[int], power: float, expected_step: int
) -> None:
    """Test the conversion of power to a step."""
    logic = StepDimmerLogic(brightness_steps)
    assert logic._power_to_step(power) == expected_step


@pytest.mark.parametrize(
    "brightness, expected_step",
    [
        (0, 0),
        (1, 0),
        (63, 1),  # ~25%
        (127, 2),  # ~50%
        (191, 3),  # ~75%
        (255, 4),  # 100%
    ],
)
def test_brightness_to_step(
    brightness_steps: list[int], brightness: int, expected_step: int
) -> None:
    """Test the conversion of brightness to a step."""
    logic = StepDimmerLogic(brightness_steps)
    assert logic._brightness_to_step(brightness) == expected_step


@pytest.mark.parametrize(
    "current_power, target_brightness, expected_toggles",
    [
        # No change
        (10, 63, 0),  # Step 1 to Step 1
        (50, 191, 0),  # Step 3 to Step 3
        # Move up
        (10, 127, 1),  # Step 1 to Step 2
        (10, 255, 3),  # Step 1 to Step 4
        (0, 127, 2),  # Off to Step 2
        # Move down (cycle)
        (100, 63, 1),  # Step 4 to Step 1
        (50, 63, 2),  # Step 3 to Step 1
    ],
)
def test_get_toggles_for_brightness(
    brightness_steps: list[int],
    current_power: float,
    target_brightness: int,
    expected_toggles: int,
) -> None:
    """Test the calculation of toggles needed."""
    logic = StepDimmerLogic(brightness_steps)
    assert (
        logic.get_toggles_for_brightness(current_power, target_brightness)
        == expected_toggles
    )
