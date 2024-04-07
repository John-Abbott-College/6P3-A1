from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand
from fan_control import FanController
from led_pwm import LEDController
from temp_humi_sensor import TempHumiController
from mock_fan_control import MockFanController
from mock_led_control import MockLEDController
from mock_temp_humi_control import MockTempHumiController
import os
from dotenv import load_dotenv

load_dotenv()
env = os.environ["MODE"]
if env == "prod":
    humidityTemperatureSensor = TempHumiController(4, "AHT20", AReading.Type.TEMPERATURE)
    fanController = FanController(16, ACommand.Type.FAN, "ON")
    ledController = LEDController(18, ACommand.Type.LIGHT_PULSE, "ON")
else:
    humidityTemperatureSensor = MockTempHumiController(4, "AHT20", AReading.Type.TEMPERATURE)
    fanController = MockFanController(16, ACommand.Type.FAN, "ON")
    ledController = MockLEDController(18, ACommand.Type.LIGHT_PULSE, "ON")

class DeviceController:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

        :return List[ISensor]: List of initialized sensors.
        """

        return [
            humidityTemperatureSensor
        ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor

        :return list[IActuator]: List of initialized actuators.
        """

        return [
            fanController,
            ledController
        ]

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors. 

        :return list[AReading]: a list containing all readings collected from sensors.
        """

        readings: list[AReading] = []
        for sensor in self._sensors:
            for reading in sensor.read_sensor():
                readings.append(reading)

        return readings

    def control_actuators(self, commands: list[ACommand]) -> None:
        """Controls actuators according to a list of commands. Each command is applied to it's respective actuator.

        :param list[ACommand] commands: List of commands to be dispatched to corresponding actuators.
        """
        
        for command in commands:
            for actuator in self._actuators:
                if actuator.validate_command(command):
                    actuator.control_actuator(command.value)
                    break


if __name__ == "__main__":
    """This script is intented to be used as a module, however, code below can be used for testing.
    """

    device_manager = DeviceController()
    TEST_SLEEP_TIME = 2

    while True:
        print(device_manager.read_sensors())

        commands = [
            #ACommand(ACommand.Type.FAN, "ON"),
            ACommand(ACommand.Type.LIGHT_ON_OFF, "ON")
        ]

        device_manager.control_actuators(commands)
        sleep(TEST_SLEEP_TIME)

        commands = [
            #ACommand(ACommand.Type.FAN, "OFF"),
            ACommand(ACommand.Type.LIGHT_ON_OFF, "OFF")
        ]
