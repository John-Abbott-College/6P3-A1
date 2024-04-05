from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand

from fan_actuator import FanActuator
from led_actuator import LEDActuator
from temperature_sensor import TemperatureSensor
from humidity_sensor import HumiditiySensor

class DeviceController:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

    :return List[ISensor]: List of initialized sensors.
    """
    def _initialize_sensors(self) -> list[ISensor]:
        return [
            TemperatureSensor(26, "AHT20", AReading.Type.TEMPERATURE),
            HumiditiySensor(26, "AHT20", AReading.Type.HUMIDITY),
        ]

    """Initializes all actuators and returns them as a list. Intended to be used in class constructor

    :return list[IActuator]: List of initialized actuators.
    """
    def _initialize_actuators(self) -> list[IActuator]:
        return [
            FanActuator(5, ACommand.Type.FAN, "0"),
            FanActuator(5, ACommand.Type.LIGHT_PULSE, "0"),
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

    while True:
        print(device_manager.read_sensors())

        fake_command = ACommand(
            ACommand.Type.FAN, "1")

        device_manager.control_actuators([fake_command])

        sleep(TEST_SLEEP_TIME)
