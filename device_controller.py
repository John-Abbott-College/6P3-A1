#!/usr/bin/env python
from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand
from fan_control import FanActuator
from led_pwm import LEDActuator 
from temp_humi_sensor import TempHumiditySensor
from temp_humi_sensor_dev import TempHumiditySensorDev
from fan_control_dev import FanActuatorDev
from led_pwm_dev import LEDActuatorDev
from dotenv import load_dotenv
from dotenv import dotenv_values
import os

class DeviceController:

    def __init__(self) -> None:
        load_dotenv()
        config = dotenv_values(".env")
        print("Dev mode is " +config["DEV"])
        print("Prod mode is " +config["PROD"])

        
        if config["PROD"] == "True":
            self.dev = False
            self._sensors: list[ISensor] = self._initialize_sensors()
            self._actuators: list[IActuator] = self._initialize_actuators()
        elif config["DEV"] == "True":
            self.dev = True
            self._sensors_dev: list[ISensor] = self._initialize_sensors_dev()
            self._actuators_dev: list[IActuator] = self._initialize_actuators_dev()

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
    
    def _initialize_sensors_dev(self) -> list[ISensor]:
        return [
            TempHumiditySensorDev(
                type = AReading.Type.TEMPERATURE
            ),
            TempHumiditySensorDev(
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
    
    def _initialize_actuators_dev(self) -> list[IActuator]:
        return [
            FanActuatorDev(
                type=ACommand.Type.FAN
            ),
            LEDActuatorDev(
                type=ACommand.Type.LIGHT_PULSE
            )
        ]

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors. 

        :return list[AReading]: a list containing all readings collected from sensors.
        """

        if not self.dev:

            readings: list[AReading] = [
            sensor.read_sensor() for sensor in self._sensors 
            ]
        else:
            readings: list[AReading] = [
            sensor.read_sensor() for sensor in self._sensors_dev 
            ]

        return readings
    
    

    def control_actuators(self, commands: list[ACommand]) -> None:
        """Controls actuators according to a list of commands. Each command is applied to it's respective actuator.

        :param list[ACommand] commands: List of commands to be dispatched to corresponding actuators.
        """
        count = 1
        print("************************************")
        if not self.dev:
            for command in commands:
                print("Command #"+str(count))
                count = count+1
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
                
                print("************************************")
            

        else:
            for command in commands:
                print("Command #"+str(count))
                count = count+1
                if  command.target_type == ACommand.Type.FAN:
                    if not self._actuators_dev[0].validate_command(command):
                        self._actuators_dev[0].control_actuator(command.value)
                    else:
                        print("invalid command")
                elif command.target_type == ACommand.Type.LIGHT_PULSE:
                    if not self._actuators_dev[1].validate_command(command):
                        self._actuators_dev[1].control_actuator(command.value)
                        print("LED Pulsed for "+str(command.value)+" seconds")
                    else:
                        print("invalid command")

                print("************************************")


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
