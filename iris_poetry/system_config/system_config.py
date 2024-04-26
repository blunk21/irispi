import json
import time
import os
import requests
from dotenv import load_dotenv

current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
env_filepath = os.path.join(parent_dir,".env")

print(env_filepath)

load_dotenv(env_filepath)


class SystemConfig:
    def __init__(self):
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
            with open(os.path.join(curdir, "config.json"), "w") as fo:
                fo.write(contents)
        json_cfg = json.loads(contents)
        self.last_updated = self._load_config(json_cfg)

    def _load_config(self, cfg: dict) -> int:
        self.alarm1 = cfg["alrm1"]
        self.alarm2 = cfg["alrm2"]
        self.duration1 = cfg["dur1"]
        self.duration2 = cfg["dur2"]
        self.measurement_frequency = cfg["mes_freq"]
        self.config_id = cfg["id"]

        return round(time.time())

    def update_config(self):
        environment = os.getenv("IRIS_ENVIRONMENT")
        headers = {"Content-Type":"application/json"}
        url = "http://" + os.getenv("IRIS_URL_"+environment) + "/configs/" + str(self.config_id) + "/"
        print(url)
        
        response = requests.request("GET",url=url,headers=headers)
        
