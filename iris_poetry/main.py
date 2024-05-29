from multiprocessing import Process, Manager
from irrigation.irrigation import process_irrigation

from system_config.config_manager import process_configuration_manager


if __name__ == "__main__":
    with Manager() as manager:
        q_measurement_data = manager.Queue()
        q_measurement_frequency = manager.Queue()
        q_configuration = manager.Queue()

        p_configuration = Process(
            target=process_configuration_manager, args=(q_configuration,)
        )
        p_sensor = Process(target=process_irrigation, args=(q_configuration,))

        p_configuration.start()
        p_sensor.start()

        p_configuration.join()
        p_sensor.join()
