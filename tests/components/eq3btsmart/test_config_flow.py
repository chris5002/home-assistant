"""Test for Eq3BTSmart Config flow."""
from unittest.mock import patch

from homeassistant import config_entries
from homeassistant.components.eq3btsmart.const import DOMAIN
from homeassistant.const import CONF_MAC
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
        result_user_confirm = await hass.config_entries.flow.async_configure(
            result["flow_id"], user_input={}
        )
    assert result_user_confirm["type"] == FlowResultType.CREATE_ENTRY
    assert result_user_confirm["title"] == "CC-RT-BLE"
    assert result_user_confirm["data"] == {}
    assert result_user_confirm["result"].unique_id == "00:11:22:33:44:55"


async def test_async_step_user_no_devices(hass: HomeAssistant):
    """Test async step user no devices discovered."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"


async def test_async_step_user_no_new_device(hass: HomeAssistant):
    """Test async step user no devices discovered with already discovered devices."""
    with patch(
        "homeassistant.components.bluetooth.async_discovered_service_info",
        return_value=[CC_RT_BLE],
    ):
        with patch(
            "homeassistant.components.eq3btsmart.config_flow.EQ3ConfigFlow._async_current_ids",
            return_value={"00:11:22:33:44:55"},
        ):
            result = await hass.config_entries.flow.async_init(
                DOMAIN, context={"source": config_entries.SOURCE_USER}
            )

    assert result["type"] == FlowResultType.ABORT
    assert result["reason"] == "no_devices_found"


async def test_async_step_user(hass: HomeAssistant):
    """Test async step user device selected."""
    with patch(
        "homeassistant.components.bluetooth.async_discovered_service_info",
        return_value=[CC_RT_BLE],
    ):
        result = await hass.config_entries.flow.async_init(
            DOMAIN, context={"source": config_entries.SOURCE_USER}
        )
    assert result["type"] == FlowResultType.FORM
    assert result["step_id"] == "user"

    result_user_selection = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input={CONF_MAC: "00:11:22:33:44:55"}
    )
    assert result_user_selection["type"] == FlowResultType.CREATE_ENTRY
    assert result_user_selection["title"] == "CC-RT-BLE"
    assert result_user_selection["data"] == {}
    assert result_user_selection["result"].unique_id == "00:11:22:33:44:55"
