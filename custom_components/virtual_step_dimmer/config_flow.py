"""Config flow for Virtual Step-Dimmer integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig,
)

from .const import (
    CONF_BRIGHTNESS_STEPS,
    CONF_SENSOR_ENTITY,
    CONF_SETTLING_DELAY_SEC,
    CONF_SWITCH_ENTITY,
    CONF_TOGGLE_DELAY_SEC,
    DEFAULT_SETTLING_DELAY_SEC,
    DEFAULT_TOGGLE_DELAY_SEC,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


class VirtualStepDimmerConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Virtual Step-Dimmer."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self.data: dict[str, Any] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            self.data.update(user_input)
            return await self.async_step_brightness()
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_SWITCH_ENTITY): EntitySelector(
                        EntitySelectorConfig(domain="switch")
                    ),
                    vol.Required(CONF_SENSOR_ENTITY): EntitySelector(
                        EntitySelectorConfig(domain="sensor")
                    ),
                }
            ),
        )

    async def async_step_brightness(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the brightness steps step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                steps_str = user_input[CONF_BRIGHTNESS_STEPS]
                steps = [int(s.strip()) for s in steps_str.split(",")]
                if not steps or any(s <= 0 for s in steps):
                    raise ValueError("Steps must be positive integers.")
                self.data.update(user_input)
                return await self.async_step_advanced()
            except (ValueError, TypeError):
                errors["base"] = "invalid_brightness_steps"

        return self.async_show_form(
            step_id="brightness",
            data_schema=vol.Schema({vol.Required(CONF_BRIGHTNESS_STEPS): str}),
            errors=errors,
        )

    async def async_step_advanced(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the advanced options step."""
        if user_input is not None:
            self.data.update(user_input)
            return self.async_create_entry(title="Virtual Step-Dimmer", data=self.data)

        return self.async_show_form(
            step_id="advanced",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_TOGGLE_DELAY_SEC,
                        default=DEFAULT_TOGGLE_DELAY_SEC,
                    ): float,
                    vol.Optional(
                        CONF_SETTLING_DELAY_SEC,
                        default=DEFAULT_SETTLING_DELAY_SEC,
                    ): float,
                }
            ),
        )
