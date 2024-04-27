import json
import time
import os
import requests
from dotenv import load_dotenv
import logging

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
env_filepath = os.path.join(parent_dir, ".env")

print(env_filepath)

load_dotenv(env_filepath)


class SystemConfig:
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.alarm1: list[int]
        self.alarm2: list[int]
        self.duration1: int
        self.duration2: int
        self.measurement_frequency: int
        self.config_id: int
        self.last_updated: int
        self._init_config()

    def _init_config(self):
        curdir = os.path.dirname(__file__)
        if os.path.exists(os.path.join(curdir, "config.json")):
            fpath = os.path.join(curdir, "config.json")
            with open(fpath, "r") as fo:
                contents = fo.read()
        else:
            fpath = os.path.join(curdir, "default_config.json")
            with open(fpath, "r") as fo:
                contents = fo.read()
                self.logger.info("Loading default config.")
            with open(os.path.join(curdir, "config.json"), "w") as fo:
                fo.write(contents)
        json_cfg = json.loads(contents)
        self.last_updated = self._load_config(json_cfg)

    def _save_configuration(self, cfg: dict):
        content = json.dumps(cfg)
        curdir = os.path.dirname(__file__)
        fpath = os.path.join(curdir, "config.json")

        with open(fpath, "w") as fo:
            fo.write(content)
        return

    def _load_config(self, cfg: dict) -> int:
        try:
            self.alarm1 = cfg["alrm1"]
            self.alarm2 = cfg["alrm2"]
            self.duration1 = cfg["dur1"]
            self.duration2 = cfg["dur2"]
            self.measurement_frequency = cfg["mes_freq"]
            self.config_id = cfg["id"]
        except KeyError:
            self.logger.error("Failed to read config, unknown key.")
            return 0
        return round(time.time())

    def update_config(self) -> bool:
        environment = os.getenv("IRIS_ENVIRONMENT")
        headers = {"Content-Type": "application/json"}
        url = (
            "http://"
            + os.getenv("IRIS_URL_" + environment)
            + "/configs/"
            + str(self.config_id)
            + "/"
        )

        response = requests.request("GET", url=url, headers=headers)
        if response.status_code != 200:
            self.logger.error("Unable to fetch configuration")
            self.logger.info(f"Status code:\t{response.status_code}")
            self.logger.info(f"Content:\t{response.text}")
            return False
        try:
            contentson = json.loads(response.text)
            self._load_config(contentson)
            self._save_configuration(contentson)
            self.logger.info("Successfully loaded configuration")
        except json.decoder.JSONDecodeError:
            self.logger.error("Unable to load new configuration")
            return False

            
