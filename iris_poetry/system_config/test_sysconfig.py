from system_config import SystemConfig
import os
import logging
from time import sleep


logger: logging.Logger = logging.getLogger("Testing")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
logger.setLevel(logging.INFO)


def test_default_cfg_loading():
    curdir = os.path.dirname(__file__)
    custom_path = os.path.join(curdir, "config.json")
    config = SystemConfig(logger=logger)
    assert config.alarm1 == [6, 15]
    assert config.duration1 == 10
    assert os.path.exists(custom_path)
    os.remove(custom_path)
    
    
def test_config_update_new_config():
    curdir = os.path.dirname(__file__)
    config_path = os.path.join(curdir, "config.json")
    if os.path.exists(config_path):
        os.remove(config_path)
    config = SystemConfig(logger=logger)
    assert config.config_id == 0
    config.update_config()
    assert config.config_id != 0
    os.remove(config_path)
    
def test_config_already_up_to_date():
    curdir = os.path.dirname(__file__)
    config_path = os.path.join(curdir, "config.json")
    if os.path.exists(config_path):
        os.remove(config_path)
    config = SystemConfig(logger=logger)
    
    assert config.config_id == 0
    
    config.update_config()
    assert config.config_id != 0
    assert config.update_config() is True
    
    
    
    
    
# TODO: test when config is up to date
