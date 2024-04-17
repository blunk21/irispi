import time
from bluepy.btle import Scanner, DefaultDelegate, ScanEntry
from typing import Optional, Union
import logging


class BleBeaconData:
    battery_state: int
    battery_voltage: int
    humidity: int
    temperature: float
    measurement_time: int


logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logging.basicConfig(level=logging.NOTSET)

logger = logging.getLogger("EyeSensor")


class EyeDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # This method is called whenever a BLE advertisement packet is received
    def handleDiscovery(self, device, isNewDev, isNewData):
        if isNewDev:
            logger.info(f"Discovered device {device.addr}")
        elif isNewData:
            logger.info(f"Received new data from {device.addr}")
        pass


class EyeSensor:
    def __init__(self, address) -> None:
        self.scanner = Scanner().withDelegate(EyeDelegate())
        self.address: str = address
        self.last_measurement: int = 0

    def __update_last_measurement(self) -> None:
        self.last_measurement = round(time.time())

    def __get_tag_data(self) -> Optional[BleBeaconData]:
        logger.info("Scanning BLE devices...")
        devices: list[ScanEntry] = self.scanner.scan(11.0)
        for dev in devices:
            if dev.addr != self.address:
                continue
            try:
                manufacturer_bytes: str = dev.scanData[ScanEntry.MANUFACTURER]
                string_data: str = manufacturer_bytes.hex()
                return process_ble_data(string_data[6:])
            except KeyError:
                return None
        return None

    def get_measurement(self) -> BleBeaconData:
        measurement: BleBeaconData = self.__get_tag_data()
        if measurement is None:
            logger.warning("Tag not found or no manufacturer data is available")
            return BleBeaconData()

        measurement.measurement_time = round(time.time())
        self.__update_last_measurement()
        return measurement


def process_ble_data(extended_data: str) -> BleBeaconData:
    data_bytes = bytes.fromhex(extended_data)
    only_battery_voltage_present_value: int = 0x80
    ble_object = BleBeaconData()

    def two_byte_to_int(b1, b2):
        """Merges two bytes into an integer."""
        return int.from_bytes([b1, b2], byteorder="big", signed=True)

    indicator_byte = data_bytes[0]
    # Battery voltage in mV = 2000 + VALUE * 10
    if indicator_byte == only_battery_voltage_present_value:
        voltage = 2000 + data_bytes[1] * 10
        ble_object.battery_voltage = voltage
        ble_object.battery_state = round(((voltage - 2000) / 1300) * 100)
        return ble_object

    index = 1

    if indicator_byte & 0x01:
        ble_object.temperature = (
            two_byte_to_int(data_bytes[index], data_bytes[index + 1]) / 100
        )
        index += 2

    if indicator_byte & 0x02:
        ble_object.humidity = data_bytes[index]
        index += 1

    if indicator_byte & 0x04:
        ble_object.magnet_state = bool(indicator_byte & 0x08)

    if indicator_byte & 0x10:
        movement_state = (data_bytes[index] & 0x80) >> 7  # Most significant bit
        movement_count = ((data_bytes[index] & 0x7F) << 8) | data_bytes[index + 1]
        ble_object.movement_sensor_state = movement_state != 0
        ble_object.movement_sensor_count = movement_count
        index += 2

    if indicator_byte & 0x20:
        pitch = data_bytes[index]  # Most significant byte
        roll = two_byte_to_int(data_bytes[index + 1], data_bytes[index + 2])
        ble_object.movement_sensor_pitch = pitch
        ble_object.movement_sensor_roll = roll
        index += 3

    if indicator_byte & 0x80:
        # Battery voltage in mV = 2000 + VALUE * 10
        voltage = 2000 + data_bytes[index] * 10
        ble_object.battery_voltage = voltage
        ble_object.battery_state = round(((voltage - 2000) / 1300) * 100)
        index += 1

    return ble_object
