import multiprocessing as mp
from multiprocessing.queues import Empty
import logging
import pickle
import time
import RPi.GPIO as GPIO
from .eye_sensor import EyeSensor, BleBeaconData
from system_config.system_config import SystemConfig

logger = mp.get_logger()
logger.name = "Irrigation"


RELAY_PIN = 23
WATER_LEVEL_PIN = 24


def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    GPIO.setup(WATER_LEVEL_PIN, GPIO.IN)


def cleanup_gpio():
    GPIO.cleanup()


def process_irrigation(configuration_queue: mp.Queue):
    # Setup logging
    logger = logging.getLogger("Irrigation")
    file_handler = logging.FileHandler("logs/process_irrigation_log.txt")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)

    # Initialize sensor and configuration
    sensor = EyeSensor(address="7c:d9:f4:1a:0e:6a", logger=logger)
    config: SystemConfig = SystemConfig()
    next_measurement_time = time.time()

    setup_gpio()

    try:
        while True:
            try:
                new_cfg_bytes = configuration_queue.get_nowait()
                config = pickle.loads(new_cfg_bytes)
                logger.info("Received new configuration in queue")
                next_measurement_time = round(
                    time.time() + config.measurement_frequency - sensor.scan_duration
                )  # Reset timer
            except Empty:
                # Timeout reached without receiving new configuration
                if round(time.time()) >= next_measurement_time:
                    mes: BleBeaconData = sensor.get_measurement()
                    logger.info(f"Got measurement: {mes.__dict__}")
                    next_measurement_time += config.measurement_frequency

            # Check current time against alarms
            current_time = time.localtime()
            if (
                current_time.tm_hour == config.alarm1[0]
                and current_time.tm_min == config.alarm1[1]
            ) or (
                current_time.tm_hour == config.alarm2[0]
                and current_time.tm_min == config.alarm2[1]
            ):
                if (
                    GPIO.input(WATER_LEVEL_PIN) == GPIO.HIGH
                ):  # Check if water level is sufficient
                    logger.info("Starting irrigation process")
                    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Turn on the water pump

                    # Determine the duration for the current alarm
                    if (
                        current_time.tm_hour == config.alarm1[0]
                        and current_time.tm_min == config.alarm1[1]
                    ):
                        duration = config.duration1
                    else:
                        duration = config.duration2

                    start_time = time.time()
                    while time.time() - start_time < duration:
                        if (
                            GPIO.input(WATER_LEVEL_PIN) == GPIO.LOW
                        ):  # Water level insufficient
                            logger.warning("Water level low! Stopping irrigation.")
                            break
                        time.sleep(1)  # Check water level every second

                    GPIO.output(RELAY_PIN, GPIO.LOW)  # Turn off the water pump
                    logger.info("Irrigation process completed")

    finally:
        cleanup_gpio()
