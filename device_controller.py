#!/usr/bin/env python

from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand

from led import PWM_LED
from temp_humi_sensor import TempHumiSensor
from fan import Fan

class DeviceController:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

        :return List[ISensor]: List of initialized sensors.
        """

        return [
            TempHumiSensor(1, "AH20", AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, 1))
        ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor

        :return list[IActuator]: List of initialized actuators.
        """

        return [
            PWM_LED(12, ACommand(ACommand.Type.LIGHT_PULSE, "5")),
            Fan(18, ACommand(ACommand.Type.FAN, "4"))
        ]

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors. 

        :return list[AReading]: a list containing all readings collected from sensors.
        """
        readings: list[AReading] = [sensor.read_sensor() for sensor in self._sensors]

        return readings

    def control_actuators(self, commands: list[ACommand]) -> None:
        """Controls actuators according to a list of commands. Each command is applied to it's respective actuator.

        :param list[ACommand] commands: List of commands to be dispatched to corresponding actuators.
        """
        for index, actuator in enumerate(self._actuators):
            actuator.control_actuator(commands[index % len(commands)].value)


if __name__ == "__main__":
    """This script is intented to be used as a module, however, code below can be used for testing.
    """

    device_manager = DeviceController()

    TEST_SLEEP_TIME = 2

    while True:
        print(device_manager.read_sensors())

        fake_command = ACommand(
            ACommand.Type.FAN, "replace with a valid command value")

        device_manager.control_actuators([fake_command])

        sleep(TEST_SLEEP_TIME)
