"""Test for Eq3BTSmart Config flow."""
from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.components.eq3btsmart.const import DOMAIN
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from . import CC_RT_BLE


async def test_async_step_bluetooth(hass: HomeAssistant):
    """Test discovery via bluetooth."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_BLUETOOTH}, data=CC_RT_BLE
    )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "bluetooth_confirm"
    with patch(
        "homeassistant.components.eq3btsmart.async_setup_entry", return_value=True
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )
    assert result2["type"] == FlowResultType.CREATE_ENTRY
    assert result2["title"] == "CC-RT-BLE"
    assert result2["data"] == {}
    assert result2["result"].unique_id == "00:11:22:33:44:55"
