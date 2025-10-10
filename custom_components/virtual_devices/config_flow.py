"""Config flow for Virtual Devices integration."""

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

from .const import CONF_SENSOR_ENTITY, CONF_SWITCH_ENTITY, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SWITCH_ENTITY): EntitySelector(
            EntitySelectorConfig(domain="switch")
        ),
        vol.Required(CONF_SENSOR_ENTITY): EntitySelector(
            EntitySelectorConfig(domain="sensor")
        ),
    }
)


class VirtualDevicesConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Virtual Devices."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Virtual Devices", data=user_input)

        return self.async_show_form(step_id="user", data_schema=STEP_USER_DATA_SCHEMA)
