from time import sleep
from dotenv import dotenv_values
from sensors import ISensor, AReading
from actuators import IActuator, ACommand
import datetime
import csv



class DeviceController:

    def __init__(self) -> None:
        self._env = dotenv_values(".env")
        self._sensors: list[ISensor] = self._initialize_sensors()

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

        :return List[ISensor]: List of initialized sensors.
        """

        if self._env["ENVIRONMENT"] == "DEVELOPMENT":
            print("Loading DEVELOPMENT sensors...")
            from mock_sensors_lab5 import MockSensor
            return [
                MockSensor(4, "AHT20", AReading.Type.TEMPERATURE),
                MockSensor(4, "AHT20", AReading.Type.HUMIDITY),
                MockSensor(4, "reTerminal", AReading.Type.LUMINOSITY),
            ]

        elif self._env["ENVIRONMENT"] == "PRODUCTION":
            print("Loading PRODUCTION sensors...")
            from sensors_lab5 import TemperatureHumiditySensor, ReTerminalSensor 
            return [
                TemperatureHumiditySensor(4, "AHT20", AReading.Type.TEMPERATURE),
                TemperatureHumiditySensor(4, "AHT20", AReading.Type.HUMIDITY),
                ReTerminalSensor(4, "reTerminal", AReading.Type.LUMINOSITY),
            ]

        else:
            print("Error: Missing 'ENVIRONMENT' key. No sensors initialized.")
            return []

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors.

        :return list[AReading]: a list containing all readings collected from sensors.
        """
        readings: list[AReading] = []
        for sensor in self._sensors:
            readings.extend(sensor.read_sensor())

        timestamp = datetime.datetime.now().time()
        with open("measurements.csv", "a") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",")
            for reading in readings:
                csvwriter.writerow((timestamp, reading.value, reading.reading_unit, reading.reading_type))

        return readings


def main():
    """Measures real time temperature, humidity, and luminosity recorded by the pi.

    Examples:
        python lab5.py
    """

    device_controller = DeviceController()

    TEST_SLEEP_TIME = 1

    while True:
        print(device_controller.read_sensors())
        sleep(TEST_SLEEP_TIME)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass