from time import sleep
from .system_config import SystemConfig
import multiprocessing as mp
import pickle
import logging


def process_configuration_manager(config_queue: mp.Queue):
    process_logger: logging.Logger = logging.getLogger("ConfigManager")

    file_handler = logging.FileHandler("logs/process_config_manager_log.txt")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    process_logger.addHandler(file_handler)
    process_logger.setLevel(logging.INFO)
    config = SystemConfig(logger=process_logger)

    pickled_cfg = pickle.dumps(config)

    while True:
        if config.update_config():
            config_queue.put(pickled_cfg)
            process_logger.info("Put new config into queue")
        process_logger.info(f"Sleeping for {config.measurement_frequency} seconds.")
        sleep(config.measurement_frequency)
