#!/usr/bin/env python3
from fan_control import FanActuator
from led_pwm import LEDActuator
from temp_humi_sensor import TempHumiditySensor

from actuators import IActuator, ACommand
from sensors import ISensor, AReading
from time import sleep


class Device_Controller:
    def __init__(self) -> None:
        self._initialize_sensors()
        self._initialize_actuators()

    def _initialize_sensors(self) -> None:
        sensor = TempHumiditySensor(model="Temp and Humidity", type=AReading.Type.TEMPERATURE)
        self.sensors = [sensor]

    def _initialize_actuators(self) -> None:
        led = LEDActuator(gpio=12, type=ACommand.Type.LIGHT_ON_OFF)
        fan = FanActuator(gpio=16, type=ACommand.Type.FAN)
        self._actuators = [led, fan]

    def control_actuator(self, actuator: IActuator, command: ACommand) -> None:
        success = actuator.control_actuator(command)

        if not success:
            print(f"Failed to control actuator {actuator} with command {command}")

    def control_actuators(self, commands) -> None:
        for actuator in self._actuators:
            for command in commands:
                if actuator.validate_command(command):
                    self.control_actuator(actuator, command.value)
        

    def read_sensors(self) -> None:
        readings: list[AReading] = []

        for sensor in self.sensors:
            fresh_readings = sensor.read_sensor()
            readings += fresh_readings
            print(f"Latest reading for {sensor}: {fresh_readings}")

    def loop(self):

        commands = [
            ACommand(ACommand.Type.LIGHT_ON_OFF, "1"),
            ACommand(ACommand.Type.FAN, "1"),
            ACommand(ACommand.Type.LIGHT_ON_OFF, "0"),
            ACommand(ACommand.Type.FAN, "0")
        ]

        while True:
            self.read_sensors()
            self.control_actuators(commands)
            sleep(2)


def main():
    controller = Device_Controller()
    controller.loop()


if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        pass
