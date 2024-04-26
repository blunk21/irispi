from .system_config import SystemConfig
import os
import pickle


def test_default_cfg_loading():
    curdir = os.path.dirname(__file__)
    custom_path = os.path.join(curdir, "config.json")
    config = SystemConfig()
    assert config.alarm1 == [6, 15]
    assert config.duration1 == 10
    assert os.path.exists(custom_path)
    os.remove(custom_path)
    
    
def test_config_update():
    curdir = os.path.dirname(__file__)
    custom_path = os.path.join(curdir, "config.json")
    if os.path.exists(custom_path):
        os.remove(custom_path)
    config = SystemConfig()
    print(config.config_id)
    print("=====Initial config=====\n")
    print(config.__dict__)
    assert config.config_id == 0
    
    config.update_config()
    assert config.config_id != 0
    print(config.__dict__)
    os.remove(custom_path)
