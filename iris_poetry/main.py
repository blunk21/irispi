import multiprocessing as mp
from multiprocessing import Process, Manager
from sensor_data.sensor_data import process_sensor_data
from irrigation_manager.irrigation import process_irrigation
from system_config.config_manager import process_configuration_manager


if __name__ == "__main__":
    with Manager() as manager:
        q_measurement_data = manager.Queue()
        q_measurement_frequency = manager.Queue()
        q_configuration = manager.Queue()

        p_sensor = Process(
            target=process_sensor_data,
            args=(q_measurement_data, q_measurement_frequency, 5),
        )
        p_irrigation = Process(target=process_irrigation, args=(q_measurement_data,))
        p_configuration = Process(target=process_configuration_manager, args=(q_configuration,))

        p_sensor.start()
        p_irrigation.start()
        p_configuration.start()

        p_sensor.join()
        p_irrigation.join()
        p_configuration.join()
