from gpiozero import LED
from time import sleep
from enum import Enum
from abc import ABC, abstractmethod
from actuators import IActuator, ACommand

class Fan(IActuator):
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str):
        self.fan = LED(gpio)
        self.type = type
        self._current_state = initial_state

    def validate_command(self, command: ACommand):
        return command.target_type == self.type
    def control_actuator(self, value: str):
        
        if (value == "on"):
            self.fan.on()
            self._current_state = value
            return True
        elif (value == "off"):
            self.fan.off()
            self._current_state = value
            return True
        return False
    

if __name__ == "__main__":

    while True:
        fan.control_actuator("on")
        sleep(0.5)
        fan.control_actuator("off")
        sleep(0.5)