from .system_config import SystemConfig


def test_default_cfg_loading():
    config = SystemConfig()
    config._load_default_config()
    assert config.alarm1 == [6, 15]
    assert config.duration1 == 10
