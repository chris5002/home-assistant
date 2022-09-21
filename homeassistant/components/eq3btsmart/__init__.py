"""The eq3btsmart component."""

import logging

from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up a climate from a config entry."""

    address = entry.unique_id
    assert address is not None

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    ble_device = bluetooth.async_ble_device_from_address(hass, address.upper(), False)

    _LOGGER.info("Start async setup %s %s", address, ble_device is None)
    if not ble_device:
        raise ConfigEntryNotReady(f"Could not find Eq3 bt Smart with address {address}")
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "climate")
    )
    return True
