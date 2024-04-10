from gpiozero import PWMLED
from time import sleep
from enum import Enum
from abc import ABC, abstractmethod
from actuators import IActuator, ACommand

class MockLED(IActuator):
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str):
        self.type = type
        self._current_state = initial_state
    def validate_command(self, command: ACommand):
        return command.target_type == self.type
    def control_actuator(self, value: str):
        if value.isnumeric():
            self._current_state = value
            if (self.type == ACommand.Type.LIGHT_PULSE):
                print("pulsing")
                return True
        else:
            if (self.type == ACommand.Type.LIGHT_ON_OFF):
                if (value == "on"):
                    print("turned on")
                    return True
                elif (value == "off"):
                    print("turned off")
                    return True
                return False



