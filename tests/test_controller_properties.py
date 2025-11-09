"""Property-based tests for the Step-Dimmer Controller."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from hypothesis import given
from hypothesis import strategies as st

from custom_components.virtual_step_dimmer.const import (
    CONF_SWITCH_ENTITY,
    LIGHT_BRIGHTNESS_MAX,
)
from custom_components.virtual_step_dimmer.controller import StepDimmerController
from custom_components.virtual_step_dimmer.logic import StepDimmerLogic


@given(
    commands=st.lists(
        st.integers(min_value=0, max_value=LIGHT_BRIGHTNESS_MAX),
        min_size=1,
        max_size=10,
    )
)
@pytest.mark.asyncio
async def test_rapid_commands_are_buffered(commands: list[int]) -> None:
    """Test that only the last of a rapid series of commands is executed."""
    mock_hass = MagicMock()
    mock_hass.services.async_call = AsyncMock()
    mock_hass.async_create_task = asyncio.create_task

    # Use a real logic object to ensure the no-op path is tested correctly
    mock_logic = StepDimmerLogic([10, 20, 30])
    config = {CONF_SWITCH_ENTITY: "switch.test"}
    state_update_callback = MagicMock()

    controller = StepDimmerController(
        mock_hass, mock_logic, config, state_update_callback
    )
    controller.handle_sensor_update(0)

    with patch("asyncio.sleep", new_callable=AsyncMock):
        for brightness in commands:
            controller.set_target_brightness(brightness)
        await asyncio.sleep(0)

    last_command = commands[-1]
    # If the last command is a no-op (off -> off), no toggles should happen
    if last_command == 0:
        mock_hass.services.async_call.assert_not_called()
    else:
        mock_hass.services.async_call.assert_called()
