from sensors import ISensor, AReading
from actuators import IActuator, ACommand
from time import sleep
import os
from dotenv import load_dotenv


load_dotenv() 

if os.getenv("ENVIRONMENT_MODE") == "prod":
    from fan_control import FanActuator
    from led_pwm import LEDActuator
    from temp_humi_sensor import TempHumiditySensor
else:
    from mock_controllers.mock_temp_humi import (MockTempHumiditySensor as TempHumiditySensor)
    from mock_controllers.mock_led import MockLEDActuator as LEDActuator
    from mock_controllers.mock_fan import MockFanActuator as FanActuator


class DeviceController:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

        :return List[ISensor]: List of initialized sensors.
        """
        return [
            TempHumiditySensor(address=0x38, bus=4, model="AHT20", type=AReading)
        ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor

        :return list[IActuator]: List of initialized actuators.
        """
        return [
            FanActuator(gpio=16, type=ACommand.Type.FAN),
            LEDActuator(18, ACommand.Type.LIGHT_PULSE, "2")
        ]

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors. 

        :return list[AReading]: a list containing all readings collected from sensors.
        """
        readings: list[AReading] = []
        for sensor in self._sensors:
            readings.extend(sensor.read_sensor())
        return readings

    def control_actuators(self, commands: list[ACommand]) -> None:
        """Controls actuators according to a list of commands. Each command is applied to it's respective actuator.

        :param list[ACommand] commands: List of commands to be dispatched to corresponding actuators.
        """
        for command in commands:
            for actuator in self._actuators:
                if actuator.validate_command(command.type):
                    actuator.control_actuator(command.value)
                    break

if __name__ == "__main__":
    """This script is intended to be used as a module, however, code below can be used for testing.
    """
  
    device_manager = DeviceController()

    TEST_SLEEP_TIME = 2

    while True:
        print(device_manager.read_sensors())

        command = ACommand(ACommand.Type.FAN, "1")

        device_manager.control_actuators([command])

        sleep(TEST_SLEEP_TIME)
