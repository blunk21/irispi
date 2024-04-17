from time import sleep
from multiprocessing import Queue
from sensor_data.eye_sensor import BleBeaconData
import multiprocessing as mp
from process_message import ProcessMessage

logger = mp.get_logger()
logger.name = "Irrigation"

def irrigation_process(mes_queue: Queue):
    while True:
        if not mes_queue.empty():
            print("received ble data")
            measurement: ProcessMessage= mes_queue.get()
            print("Received new message in queue")
            print(f"Type: {measurement.type}")
            print(f"Source: {measurement.source}")
            print(f"Payload: {measurement.payload}")
        sleep(1)