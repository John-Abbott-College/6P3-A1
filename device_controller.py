#!/usr/bin/env python
from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand
from fan_control import FanActuator
from led_pwm import LEDActuator 
from temp_humi_sensor import TempHumiditySensor
 

class DeviceController:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

        :return List[ISensor]: List of initialized sensors.
        """

        return [
            TempHumiditySensor(
                type = AReading.Type.TEMPERATURE
            ),
            TempHumiditySensor(
                type = AReading.Type.HUMIDITY
            )
        ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor

        :return list[IActuator]: List of initialized actuators.
        """

        return [
            FanActuator(
                gpio=16,
                type=ACommand.Type.FAN
            ),
            LEDActuator(
                gpio=12,
                type=ACommand.Type.LIGHT_PULSE
            )
        ]

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors. 

        :return list[AReading]: a list containing all readings collected from sensors.
        """
        readings: list[AReading] = [
            sensor.read_sensor() for sensor in self._sensors 
        ]

        return readings

    def control_actuators(self, commands: list[ACommand]) -> None:
        """Controls actuators according to a list of commands. Each command is applied to it's respective actuator.

        :param list[ACommand] commands: List of commands to be dispatched to corresponding actuators.
        """
        for command in commands:
                if  command.target_type == ACommand.Type.FAN:
                    if not self._actuators[0].validate_command(command):
                        self._actuators[0].control_actuator(command.value)
                    else:
                        print("invalid command")
                elif command.target_type == ACommand.Type.LIGHT_PULSE:
                    if not self._actuators[1].validate_command(command):
                        self._actuators[1].control_actuator(command.value)
                        print("LED Pulsed for "+str(command.value)+" seconds")
                    else:
                        print("invalid command")

            




if __name__ == "__main__":
    """This script is intented to be used as a module, however, code below can be used for testing.
    """

    device_manager = DeviceController()

    TEST_SLEEP_TIME = 2

    while True:
        sensor_data = device_manager.read_sensors()
        print("====================================")
        print(str(sensor_data[0])+"\n"+str(sensor_data[1]))
        print("====================================")

        fake_command = ACommand(
            ACommand.Type.FAN, 1)
        fake_command2 = ACommand(
            ACommand.Type.FAN, 0)
        fake_command3 = ACommand(
            ACommand.Type.LIGHT_PULSE, 1)

        device_manager.control_actuators([fake_command,fake_command3])
        sleep(TEST_SLEEP_TIME)
        device_manager.control_actuators([fake_command2])
        sleep(TEST_SLEEP_TIME)
