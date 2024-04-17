import multiprocessing as mp
from multiprocessing import Process, Manager
from sensor_data.sensor_data import sensor_data_process
from irrigation_manager.irrigation import irrigation_process


if __name__ == "__main__":
    with Manager() as manager:
        q_measurement_data = manager.Queue()
        q_measurement_frequency = manager.Queue()

        p_sensor = Process(
            target=sensor_data_process,
            args=(q_measurement_data, q_measurement_frequency, 5),
        )
        p_irrigation = Process(target=irrigation_process, args=(q_measurement_data,))

        p_sensor.start()
        p_irrigation.start()

        p_sensor.join()
        p_irrigation.join()
