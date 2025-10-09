"""Test the config flow for Virtual Devices."""

from unittest.mock import patch

import pytest
from homeassistant import config_entries, setup
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType
from homeassistant.loader import Integration

from custom_components.virtual_devices.const import DOMAIN


async def test_form(hass: HomeAssistant) -> None:
    """Test we get the form."""
    await setup.async_setup_component(hass, "persistent_notification", {})

    with patch(
        "homeassistant.loader.async_get_integrations",
        return_value={
            DOMAIN: Integration(
                hass,
                "custom_components.virtual_devices",
                None,
                {"name": "Virtual Devices", "domain": DOMAIN, "requirements": []},
            )
        },
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
        assert result["type"] is FlowResultType.FORM
        assert result["errors"] is None

    with patch(
        "homeassistant.config_entries.ConfigEntries.async_setup",
        return_value=True,
    ) as mock_setup:
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            {},
        )
        await hass.async_block_till_done()

    assert result2["type"] is FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Virtual Devices"
    assert result2["data"] == {}
    assert len(mock_setup.mock_calls) == 1
