#!/usr/bin/env python

from gpiozero import Motor
from gpiozero import OutputDevice

from actuators import ACommand, IActuator

from time import sleep

class Fan(IActuator): 
    _current_state: str
    type: ACommand.Type

    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str = "OFF") -> None:
        self.fan = OutputDevice(gpio, active_high=True, initial_value=False)

    def validate_command(self, command: ACommand) -> bool:
        return self.type == command.type

    def control_actuator(self, value: str) -> bool:
        spinTime = int(value) if value.isdecimal() else 1

        oldValue = self.fan.value
        self.fan.on()
        newValue = self.fan.value
        sleep(spinTime)
        self.fan.off()

        return oldValue == newValue


# if __name__ == "__main__":
#     fan = Fan(18, ACommand(ACommand.Type.FAN, "4"))
#     fan.control_actuator("10")
