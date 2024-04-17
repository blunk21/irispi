from time import sleep
from .eye_sensor import EyeSensor, BleBeaconData
from multiprocessing import Queue
import multiprocessing as mp
from process_message import ProcessMessage

logger = mp.get_logger()
logger.name = "SensorData"


def sensor_data_process(
    measurement_queue: Queue,
    freq_queue: Queue,
    measurement_freq: int,
):
    sensor = EyeSensor(address="7c:d9:f4:1a:0e:6a")
    while True:
        measurement: BleBeaconData = sensor.get_measurement()
        new_message = ProcessMessage()
        new_message.type = "ble_sensor_measurement"
        new_message.source = sensor_data_process.__name__
        new_message.payload = measurement.__dict__
        measurement_queue.put(new_message)

        if not freq_queue.empty():
            new_freq: int = freq_queue.get()
            if not isinstance(new_freq, int):
                logger.error("Received measurement frequency is not 'int'")

            else:
                measurement_freq = new_freq

        sleep(measurement_freq)
