from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand
from temp_humi_sensor import TempHumiditySensor
from fan_control import FanActuator
from led_pwm import LEDActuator
from dotenv import dotenv_values
from mock_fan import MockFanActuator
from mock_light import MockLEDActuator


class DeviceController:

    def __init__(self) -> None:
        self._environment = dotenv_values(".env")
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

        :return List[ISensor]: List of initialized sensors.
        """
        if(self._environment["PRODUCTION"] == "TRUE"):
            return [
                TempHumiditySensor(4, "AHT20", AReading.Type.TEMPERATURE)
            ]
        else:
            return [
                # mock temp humi sensor
            ]
        

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor

        :return list[IActuator]: List of initialized actuators.
        """
        if(self._environment["PRODUCTION"] == "TRUE"):
            return [
                FanActuator(16, ACommand.Type.FAN, "OFF"),
                LEDActuator(12, ACommand.Type.LIGHT_ON_OFF, "OFF")
            ]
        else:
            return [
                MockFanActuator(16, ACommand.Type.FAN, "OFF"),
                MockLEDActuator(12, ACommand.Type.LIGHT_ON_OFF, "OFF"),
                MockLEDActuator(12, ACommand.Type.LIGHT_PULSE, "OFF")
            ]

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors. 

        :return list[AReading]: a list containing all readings collected from sensors.
        """
        readings: list[AReading] = []
        for sensor in self._sensors:
            sensor_readings = sensor.read_sensor()
            readings.extend(sensor_readings)

        return readings

    def control_actuators(self, commands: list[ACommand]) -> None:
        """Controls actuators according to a list of commands. Each command is applied to it's respective actuator.

        :param list[ACommand] commands: List of commands to be dispatched to corresponding actuators.
        """
        for command in commands:
            index = -1
            for actuator in self._actuators:
                if (actuator.type == command.target_type):
                    index = self._actuators.index(actuator)

            if(index == -1):
                print(f"Can't execute command '{command.value}' for {command.target_type} because the actuator doesn't exist.")
            else:
                if(self._actuators[index].validate_command(command)):
                    self._actuators[index].control_actuator(command.value)


if __name__ == "__main__":
    """This script is intented to be used as a module, however, code below can be used for testing.
    """
    device_manager = DeviceController()

    TEST_SLEEP_TIME = 2

    value = "ON"
    pulse = "0"

    while True:
        print(device_manager.read_sensors())

        if(device_manager._environment["PRODUCTION"] == "TRUE"):
            fake_command = ACommand(ACommand.Type.FAN, value)
            fake_command2 = ACommand(ACommand.Type.LIGHT_ON_OFF, value)
            device_manager.control_actuators([fake_command, fake_command2]) 
        else:
            fake_command = ACommand(ACommand.Type.FAN, value)
            fake_command2 = ACommand(ACommand.Type.LIGHT_ON_OFF, value)
            fake_command3 = ACommand(ACommand.Type.LIGHT_PULSE, pulse)
            device_manager.control_actuators([fake_command, fake_command2, fake_command3]) 

        sleep(TEST_SLEEP_TIME)

        value = "ON" if value != "ON" else "OFF"
        pulse = "0" if pulse != "0" else "1"
