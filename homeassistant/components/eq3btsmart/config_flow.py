"""Config flow for eq3bt integration."""
from __future__ import annotations

import dataclasses
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components import bluetooth, onboarding
from homeassistant.components.bluetooth.models import BluetoothServiceInfoBleak
from homeassistant.const import CONF_MAC
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@dataclasses.dataclass
class Discovery:
    """A discovered bluetooth device."""

    title: str
    discovery_info: BluetoothServiceInfoBleak


class EQ3ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Example config flow."""

    def __init__(self) -> None:
        """Init the Config flow for a eq3 ble device."""
        self._discovery_info: BluetoothServiceInfoBleak | None = None
        self._discovered_devices: dict[str, Discovery] = {}

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the config flow step user."""
        if user_input is not None:
            address = user_input[CONF_MAC]
            await self.async_set_unique_id(address, raise_on_progress=False)
            self._abort_if_unique_id_configured()
            discovery = self._discovered_devices[address]

            self.context["title_placeholders"] = {"name": discovery.title}
            self._discovery_info = discovery.discovery_info
            return self._async_get_or_create_entry()

        current_addresses = self._async_current_ids()
        for discovery_info in bluetooth.async_discovered_service_info(self.hass, False):
            address = discovery_info.address
            _LOGGER.info(
                "Device %s, %s", discovery_info.address, discovery_info.connectable
            )
            if address in current_addresses or address in self._discovered_devices:
                continue
            self._discovered_devices[address] = Discovery(
                title=discovery_info.name,
                discovery_info=discovery_info,
            )

        if not self._discovered_devices:
            return self.async_abort(reason="no_devices_found")

        titles = {
            address: discovery.title
            for (address, discovery) in self._discovered_devices.items()
        }
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_MAC): vol.In(titles)}),
        )

    async def async_step_bluetooth(self, discovery_info) -> FlowResult:
        """Handle the bluetooth discovery step."""
        _LOGGER.debug("Discovered eQ3 thermostat using bluetooth: %s", discovery_info)

        await self.async_set_unique_id(discovery_info.address)
        self._abort_if_unique_id_configured()

        self.context["title_placeholders"] = {"name": discovery_info.name}
        self._discovery_info = discovery_info

        return await self.async_step_bluetooth_confirm()

    async def async_step_bluetooth_confirm(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Confirm discovery."""
        if user_input is not None or not onboarding.async_is_onboarded(self.hass):
            return self._async_get_or_create_entry()

        self._set_confirm_only()
        return self.async_show_form(
            step_id="bluetooth_confirm",
            description_placeholders=self.context["title_placeholders"],
        )

    def _async_get_or_create_entry(self):
        if entry_id := self.context.get("entry_id"):
            entry = self.hass.config_entries.async_get_entry(entry_id)
            assert entry is not None

            return self.async_abort(reason="reauth_successful")

        return self.async_create_entry(
            title=self.context["title_placeholders"]["name"],
            data={},
        )
