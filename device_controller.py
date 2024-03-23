#!/usr/bin/env python3

from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand
from fan_control import FanController, FAN_GPIO_PIN
from led_pwm import LEDController, LED_GPIO_PIN
from temp_humi_sensor import TemperatureHumiditySensor, BUS

class DeviceController:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

        :return List[ISensor]: List of initialized sensors.
        """

        return [
            TemperatureHumiditySensor(gpio=BUS, model="AHT20", type=AReading.Type.TEMPERATURE),
            TemperatureHumiditySensor(gpio=BUS, model="AHT20", type=AReading.Type.HUMIDITY)
        ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor

        :return list[IActuator]: List of initialized actuators.
        """

        return [
            FanController(gpio=FAN_GPIO_PIN, type= ACommand.Type.FAN, initial_state= "off"),
            LEDController(gpio=LED_GPIO_PIN, type=ACommand.Type.LIGHT_PULSE, initial_state= "off"),
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
        for command in commands:
            for actuator in self._actuators:
                if actuator.type == command.target_type:
                    if actuator.validate_command(command= command):
                        actuator.control_actuator(command.value)
                        print(f"Executed command on {actuator.type}: {command.value}")
                    else:
                        print(f"Invalid command for actuator type {actuator.type}")
                    break
            else:
                print(f"No actuator found for command type {command.target_type}")


if __name__ == "__main__":
    """This script is intented to be used as a module, however, code below can be used for testing.
    """

    device_manager = DeviceController()

    TEST_SLEEP_TIME = 2

    while True:
        print(device_manager.read_sensors())

        fake_command = ACommand(
            ACommand.Type.LIGHT_PULSE, "2")

        device_manager.control_actuators([fake_command])

        sleep(TEST_SLEEP_TIME)
        
        fake_command = ACommand(
            ACommand.Type.FAN, "off")
        device_manager.control_actuators([fake_command])

        sleep(TEST_SLEEP_TIME)

