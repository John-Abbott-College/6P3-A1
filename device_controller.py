from sensors import ISensor, AReading
from actuators import IActuator, ACommand
from time import sleep
from dotenv import load_dotenv
from os import getenv

load_dotenv()


env = getenv('ENV')

if env == "DEV":
    from SimulationClasses import DevSimulationTempHumSensor, DevFanActuation, DevLEDActuation
else:
    from fan_control import FanActuator
    from led_pwm import LEDActuator
    from temp_humi_sensor import TempHumiditySensor

class Device_Controller:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> list[ISensor]:
            """Initializes all sensors and returns them as a list. Intended to be used in class constructor.

            :return List[ISensor]: List of initialized sensors.
            """
            if env == "DEV":
                return [
               DevSimulationTempHumSensor()
                # Instantiate each sensor inside this list, separate items by comma.
            ]
                
            return [
                # For testing

                DevSimulationTempHumSensor()
                #TempHumiditySensor()
                # Instantiate each sensor inside this list, separate items by comma.
            ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor

        :return list[IActuator]: List of initialized actuators.
        """
        if env == "Dev":
            return [
                DevFanActuation(ACommand.Type.FAN),
                DevLEDActuation(ACommand.Type.LIGHT_PULSE, "0")
            ]
        return [
            # for testing
            #FanActuator(16, ACommand.Type.FAN, "0"),
            #LEDActuator(12, ACommand.Type.LIGHT_PULSE, "0"),
            # Instantiate each actuator inside this list, separate items by comma.

            DevFanActuation(ACommand.Type.FAN),
            DevLEDActuation(ACommand.Type.LIGHT_ON_OFF, "0")
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
        for actuator in self._actuators:
            for command in commands:
                if actuator.type == command.target_type:
                    actuator.control_actuator(command.value)
    
    