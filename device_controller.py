from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand
from temp_humi_sensor import TempHumiditySensor
from led_pwm import LEDActuator
from fan_control import FanActuator

class DeviceController:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list."""
        return [
            TempHumiditySensor()
        ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list."""
        return [
            FanActuator(gpio=16),
            LEDActuator(gpio=12),
        ]

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors."""
        readings: list[AReading] = []
        for sensor in self._sensors:
            readings.extend(sensor.read_sensor())
        return readings

    def control_actuators(self, commands: list[ACommand]) -> None:
        """Controls actuators according to a list of commands."""
        for command in commands:
            for actuator in self._actuators:
                if actuator.validate_command(command):
                    actuator.control_actuator(command.value)

if __name__ == "__main__":
    device_manager = DeviceController()

    TEST_SLEEP_TIME = 2

    while True:
        print(device_manager.read_sensors())

        fake_command_fan = ACommand(ACommand.Type.FAN, "1")
        fake_command_led = ACommand(ACommand.Type.LIGHT_PULSE, "0.5")

        device_manager.control_actuators([fake_command_fan, fake_command_led])

        sleep(TEST_SLEEP_TIME)
