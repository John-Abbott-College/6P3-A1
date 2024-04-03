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

        sensor = TempHumiditySensor(gpio=26, model="AHT20", command_type=AReading.Type.TEMPERATURE)
       
        return [
            # Instantiate each sensor inside this list, separate items by comma.
            sensor
        ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor

        :return list[IActuator]: List of initialized actuators.
        """
        return [
            FanActuator(gpio=16, command_type=ACommand.Type.FAN),
            LEDActuator(gpio=12, command_type=ACommand.Type. LIGHT_PULSE)
            # Instantiate each actuator inside this list, separate items by comma.
        ]

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors. 

        :return list[AReading]: a list containing all readings collected from sensors.
        """
        readings: list[AReading] = []
        for sensor in self._sensors:
            for total_readings in sensor.read_sensor():
                readings.append(total_readings)
                   
        return readings

    def control_actuators(self, commands: list[ACommand]) -> None:
        """Controls actuators according to a list of commands. Each command is applied to it's respective actuator.

        :param list[ACommand] commands: List of commands to be dispatched to corresponding actuators.
        """


if __name__ == "__main__":
    """This script is intented to be used as a module, however, code below can be used for testing.
    """

    device_manager = DeviceController()

    TEST_SLEEP_TIME = 2

    while True:
        print(device_manager.read_sensors())

        fake_command = ACommand(
            ACommand.Type.FAN, "on")
        
        print(f"Fan state: {fan_actuator.current_state}")
        sleep(2)
        fan_actuator.control_actuator("0")
        print(f"Fan state: {fan_actuator.current_state}")
        sleep(2)
        # device_manager.control_actuators([fake_command])

        # sleep(TEST_SLEEP_TIME)
