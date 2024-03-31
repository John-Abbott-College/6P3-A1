from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand
from temp_humi_sensor import TempController
from fan_control import FanController
from led_pwm import LEDController


class DeviceController:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

        :return List[ISensor]: List of initialized sensors.
        """

        return [
            # Instantiate each sensor inside this list, separate items by comma.
            TempController(4, "AHT20", AReading.Type.TEMPERATURE)
        ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor

        :return list[IActuator]: List of initialized actuators.
        """

        return [
            # Instantiate each actuator inside this list, separate items by comma.
            FanController(22, ACommand.Type.FAN, "OFF"),
            LEDController(16, ACommand.Type.LIGHT_PULSE, "OFF"),
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
                if actuator.validate_command(command):
                    actuator.control_actuator(command.value)
                    break


if __name__ == "__main__":
    """
    This script is intented to be used as a module, however, code below can be used for testing.
    """
    device_manager = DeviceController()
    TEST_SLEEP_TIME = 2

    while True:
        print(device_manager.read_sensors())

        commands = [
            ACommand(ACommand.Type.FAN, "ON"),
            ACommand(ACommand.Type.LIGHT_ON_OFF, "ON"),
        ]

        device_manager.control_actuators(commands)

        sleep(TEST_SLEEP_TIME)

        commands = [
            ACommand(ACommand.Type.FAN, "OFF"),
            ACommand(ACommand.Type.LIGHT_ON_OFF, "OFF"),
        ]
