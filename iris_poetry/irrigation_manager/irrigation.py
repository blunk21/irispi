from time import sleep
from multiprocessing import Queue
from sensor_data.eye_sensor import BleBeaconData
import multiprocessing as mp

logger = mp.get_logger()
logger.name = "Irrigation"

def irrigation_process(mes_queue: Queue):
    while True:
        if not mes_queue.empty():
            print("received ble data")
            beacon_data:BleBeaconData = mes_queue.get()
            print(beacon_data.__dict__)
        sleep(1)