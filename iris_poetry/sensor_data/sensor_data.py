import multiprocessing as mp
from multiprocessing.queues import Empty
import logging
import pickle
import time

# Assuming these imports are set up in your environment:
from .eye_sensor import EyeSensor, BleBeaconData
from system_config.system_config import SystemConfig

logger = mp.get_logger()
logger.name = "SensorData"


def process_sensor_data(configuration_queue: mp.Queue):
    # Setup logging
    logger = logging.getLogger("SensorData")
    file_handler = logging.FileHandler("logs/process_sensor_data_log.txt")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    # Initialize sensor and configuration
    sensor = EyeSensor(address="7c:d9:f4:1a:0e:6a", logger=logger)
    config: SystemConfig = SystemConfig()
    next_measurement_time = time.time()

    while True:
        try:
            # Block until new configuration is available or it's time for the next measurement
            new_cfg_bytes = configuration_queue.get(
                timeout=max(0, next_measurement_time - time.time())
            )
            config = pickle.loads(new_cfg_bytes)
            logger.info("Received new configuration in queue")
            next_measurement_time = round(
                time.time() + config.measurement_frequency-sensor.scan_duration
            )  # Reset timer
        except Empty:
            # Timeout reached without receiving new configuration
            if round(time.time()) >= next_measurement_time:
                mes: BleBeaconData = sensor.get_measurement()
                logger.info(f"Got measurement: {mes.__dict__}")
                next_measurement_time += config.measurement_frequency 
