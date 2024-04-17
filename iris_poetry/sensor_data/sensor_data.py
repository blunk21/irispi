from time import sleep
from .eye_sensor import EyeSensor, BleBeaconData
from multiprocessing import Queue
import multiprocessing as mp

logger = mp.get_logger()
logger.name = "SensorData"


def sensor_data_process(
    measurement_queue: Queue,
    freq_queue: Queue,
    measurement_freq: int,
):
    sensor = EyeSensor(address="7c:d9:f4:1a:0e:6a")
    while True:
        mes: BleBeaconData = sensor.get_measurement()
        measurement_queue.put(mes)

        if not freq_queue.empty():
            new_freq: int = freq_queue.get()
            if not isinstance(new_freq, int):
                logger.error("Received measurement frequency is not 'int'")

            else:
                measurement_freq = new_freq

        sleep(measurement_freq)
