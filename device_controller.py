from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand

from fan_actuator import FanActuator
from led_actuator import LEDActuator
from temperature_sensor import TemperatureSensor
from humidity_sensor import HumiditySensor

from mock_actuators import MockFanActuator, MockLEDActuator
from mock_sensors import MockHumiditySensor, MockTemperatureSensor

from dotenv import dotenv_values

class DeviceController:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

    :return List[ISensor]: List of initialized sensors.
    """
    def _initialize_sensors(self) -> list[ISensor]:
        if dotenv_values()["ENVIRONMENT"] == "PRODUCTION":
            return [
                TemperatureSensor(4, "AHT20", AReading.Type.TEMPERATURE),
                HumiditySensor(4, "AHT20", AReading.Type.HUMIDITY),
            ]
        else:
            return [
                MockTemperatureSensor(4, "AHT20", AReading.Type.TEMPERATURE),
                MockHumiditySensor(4, "AHT20", AReading.Type.HUMIDITY),
            ]

    """Initializes all actuators and returns them as a list. Intended to be used in class constructor

    :return list[IActuator]: List of initialized actuators.
    """
    def _initialize_actuators(self) -> list[IActuator]:
        if dotenv_values()["ENVIRONMENT"] == "PRODUCTION":
            return [
                FanActuator(22, ACommand.Type.FAN, "0"),
                LEDActuator(5, ACommand.Type.LIGHT_ON_OFF, "0"),
            ]
        else:
            return [
                MockFanActuator(22, ACommand.Type.FAN, "0"),
                MockLEDActuator(5, ACommand.Type.LIGHT_ON_OFF, "0"),
            ]

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors. 

        :return list[AReading]: a list containing all readings collected from sensors.
        """
        readings: list[AReading] = [
            reading
            for readings in 
            (sensor.read_sensor() for sensor in self._sensors)
            for reading in readings
        ]

        return readings

    def control_actuators(self, commands: list[ACommand]) -> None:
        """Controls actuators according to a list of commands. Each command is applied to it's respective actuator.

        :param list[ACommand] commands: List of commands to be dispatched to corresponding actuators.
        """
        for command in commands:
            for actuator in self._actuators:
                if actuator.validate_command(command):
                    actuator.control_actuator(command.value)


if __name__ == "__main__":
    """This script is intented to be used as a module, however, code below can be used for testing.
    """

    device_manager = DeviceController()

    TEST_SLEEP_TIME = 2

    fan_on = ACommand(ACommand.Type.FAN, "1")
    fan_off = ACommand(ACommand.Type.FAN, "0")

    led_pulse = ACommand(ACommand.Type.LIGHT_PULSE, "1")
    led_off = ACommand(ACommand.Type.LIGHT_ON_OFF, "0")

    while True:
        print("==================");
        print(device_manager.read_sensors())
        device_manager.control_actuators([led_off, fan_on])
        print("LED off")
        print("Fan on")

        sleep(TEST_SLEEP_TIME)

        print("==================");
        print(device_manager.read_sensors())
        device_manager.control_actuators([led_pulse, fan_off])
        print("LED pulse twice for 2s total")
        print("Fan off")

        sleep(TEST_SLEEP_TIME)
