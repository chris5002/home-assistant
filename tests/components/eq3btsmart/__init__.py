"""Definition of an eq3bt BluetoothServiceInfoBleak."""
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from homeassistant.components.bluetooth import BluetoothServiceInfoBleak

CC_RT_BLE = BluetoothServiceInfoBleak(
    name="CC-RT-BLE",
    address="00:11:22:33:44:55",
    rssi=0,
    manufacturer_data={},
    service_data={},
    service_uuids=[
        "00001800-0000-1000-8000-00805f9b34fb",
        "00001801-0000-1000-8000-00805f9b34fb",
        "0000180a-0000-1000-8000-00805f9b34fb",
        "3e135142-654f-9090-134a-a6ff5bb77046",
        "9e5d1e47-5c13-43a0-8635-82ad38a1386f",
    ],
    source="local",
    device=BLEDevice("00:11:22:33:44:55", "CC-RT-BLE"),
    advertisement=AdvertisementData(local_name="CC-RT-BLE"),
    connectable=False,
    time=0,
)
