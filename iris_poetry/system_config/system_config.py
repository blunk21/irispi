import json
import os

class SystemConfig:
    def __init__(self):
        self.alarm1: list[int]
        self.alarm2: list[int]
        self.duration1: int
        self.duration2: int
        self.measurement_frequency: int

    def _load_default_config(self):
        curdir = os.path.dirname(__file__)
        fpath = os.path.join(curdir,"default_config.json")
        with open(fpath,"r") as fo:
            contents = fo.read()

        json_cfg = json.loads(contents)
        self.alarm1 = json_cfg["alrm1"]
        self.alarm2 = json_cfg["alrm2"]
        self.duration1 = json_cfg["dur1"]
        self.duration2 = json_cfg["dur2"]
        self.measurement_frequency = json_cfg["mes_freq"]