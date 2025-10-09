"""Config flow for Virtual Devices integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigFlow
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class VirtualDevicesConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Virtual Devices."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Virtual Devices", data={})

        return self.async_show_form(step_id="user")
