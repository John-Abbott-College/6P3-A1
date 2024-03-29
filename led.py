#!/usr/bin/env python

from gpiozero import LED
from gpiozero import PWMLED

from actuators import ACommand, IActuator

from time import sleep

class PWM_LED(IActuator): 
    _current_state: str
    type: ACommand.Type

    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str = "OFF") -> None:
        self.type = type
        self._current_state = initial_state

        self.led = PWMLED(gpio)

    def validate_command(self, command: ACommand) -> bool:
        return self.type == command.type

    def control_actuator(self, value: str) -> bool:
        pulseLength = int(value) if value.isdecimal() else 2

        self.led.pulse(pulseLength / 2, pulseLength / 2, 1, False)
        return True


# if __name__ == "__main__":
#     pwm = PWM_LED(12, ACommand(ACommand.Type.LIGHT_PULSE, "5"))
#     pwm.control_actuator("h")