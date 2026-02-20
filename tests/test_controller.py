"""Test the Step-Dimmer Controller."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.virtual_step_dimmer.const import (
    CONF_SWITCH_ENTITY,
    SETTLING_DELAY_SEC,
)
from custom_components.virtual_step_dimmer.controller import StepDimmerController
from custom_components.virtual_step_dimmer.logic import StepDimmerLogic


@pytest.fixture
def mock_hass() -> MagicMock:
    """Fixture for a mock Home Assistant object."""
    hass = MagicMock()
    hass.services.async_call = AsyncMock()
    hass.async_create_task = MagicMock(side_effect=asyncio.create_task)
    return hass


@pytest.fixture
def mock_logic() -> MagicMock:
    """Fixture for a mock StepDimmerLogic object."""
    logic = MagicMock(spec=StepDimmerLogic)
    logic.get_toggles_for_brightness.return_value = 1
    logic._power_to_step.return_value = 1
    logic._step_to_brightness.return_value = 64
    return logic


@pytest.fixture
def config() -> dict:
    """Fixture for a config dictionary."""
    return {CONF_SWITCH_ENTITY: "switch.test"}


@pytest.mark.asyncio
async def test_command_buffering(
    mock_hass: MagicMock, mock_logic: MagicMock, config: dict
) -> None:
    """Test that rapid commands are buffered and the last one is executed."""
    state_update_callback = MagicMock()
    controller = StepDimmerController(
        mock_hass, mock_logic, config, state_update_callback
    )

    controller.handle_sensor_update(10)
    mock_logic.get_toggles_for_brightness.return_value = 3

    controller.set_target_brightness(127)
    controller.set_target_brightness(255)

    await asyncio.sleep(SETTLING_DELAY_SEC + 1)

    mock_logic.get_toggles_for_brightness.assert_called_once_with(10, 255)
    assert mock_hass.services.async_call.call_count == 3


@pytest.mark.asyncio
async def test_update_in_progress(
    mock_hass: MagicMock, mock_logic: MagicMock, config: dict
) -> None:
    """Test that a new task is not created if an update is already running."""
    state_update_callback = MagicMock()
    controller = StepDimmerController(
        mock_hass, mock_logic, config, state_update_callback
    )

    controller.set_target_brightness(100)
    await asyncio.sleep(0.1)

    controller.set_target_brightness(200)
    await asyncio.sleep(SETTLING_DELAY_SEC + 1)

    assert mock_hass.async_create_task.call_count == 1


@pytest.mark.asyncio
async def test_sensor_update_callback(
    mock_hass: MagicMock, mock_logic: MagicMock, config: dict
) -> None:
    """Test that the sensor update triggers the callback."""
    state_update_callback = MagicMock()
    controller = StepDimmerController(
        mock_hass, mock_logic, config, state_update_callback
    )

    controller.handle_sensor_update(25)

    mock_logic._power_to_step.assert_called_once_with(25)
    mock_logic._step_to_brightness.assert_called_once_with(1)
    state_update_callback.assert_called_once_with(25, 64)


@pytest.mark.asyncio
async def test_cancel(
    mock_hass: MagicMock, mock_logic: MagicMock, config: dict
) -> None:
    """Test that the update task can be cancelled."""
    state_update_callback = MagicMock()
    controller = StepDimmerController(
        mock_hass, mock_logic, config, state_update_callback
    )

    controller.set_target_brightness(100)
    await asyncio.sleep(0.1)

    controller.cancel()
    await asyncio.sleep(0.1)

    assert controller._update_task.cancelled()
