from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand
from temp_humi_sensor import TempHumiditySensor
from fan_control import Fan
from led_pwm import LED


class DeviceController:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

        :return List[ISensor]: List of initialized sensors.
        """
        sensor = TempHumiditySensor(gpio=0, model="AHT20", type=AReading.Type.TEMPERATURE)
        return [
           sensor
        ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor

        :return list[IActuator]: List of initialized actuators.
        """
        fan = Fan(12, ACommand.Type.FAN, "off")
        led = LED(22, ACommand.Type.LIGHT_ON_OFF, "2")
        return [
            # Instantiate each actuator inside this list, separate items by comma.
            fan, led
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


if __name__ == "__main__":
    """This script is intented to be used as a module, however, code below can be used for testing.
    """

    device_manager = DeviceController()

    TEST_SLEEP_TIME = 2

    while True:

        print(device_manager.read_sensors())

        fake_command = ACommand(
            ACommand.Type.FAN, "on")
        fake_command2 = ACommand(
            ACommand.Type.FAN, "off")
        fake_command3 = ACommand(
            ACommand.Type.LIGHT_ON_OFF, "on")
        fake_command4 = ACommand(
            ACommand.Type.LIGHT_ON_OFF, "off")
        sleep(TEST_SLEEP_TIME)
        device_manager.control_actuators([fake_command])
        device_manager.control_actuators([fake_command3])
        sleep(TEST_SLEEP_TIME)
        device_manager.control_actuators([fake_command2])
        device_manager.control_actuators([fake_command4])