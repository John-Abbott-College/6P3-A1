from gpiozero import OutputDevice
from time import sleep
from typing import Union
from abc import ABC, abstractmethod
from enum import Enum

class ACommand(ABC):
    """Abstract class for actuator command. Can be instantiated directly or inherited.
    Also defines all possible command types via enums.
    """

    class Type(str, Enum):
        """Enum defining types of actuators that can be targets for a command
        """
        FAN = 'fan'
        LIGHT_ON_OFF = 'light-on-off'
        LIGHT_PULSE = 'light-pulse'

    def __init__(self, target: Type, value: str) -> None:
        """Constructor for Command abstract class

        :param Type target: Type of command which associates a command to a type of actuator.
        :param str value: Value of command to be passed to actuator.
        """
        self.target_type = target
        self.value: str = value

    def __repr__(self) -> str:
        return f'Command setting {self.target_type} to {self.value}'

class IActuator(ABC):
    _current_state: str
    type: ACommand.Type

    @abstractmethod
    def validate_command(self, command: ACommand) -> bool:
        pass

    @abstractmethod
    def control_actuator(self, value: str) -> bool:
        pass

class FanController(IActuator):
    _current_state: str
    type: ACommand.Type  

    def __init__(self, relay_pin: int, initial_state: str = "off") -> None:
        self.relay = OutputDevice(relay_pin)
        self.type = ACommand.Type.FAN  
        self._current_state = initial_state

    def validate_command(self, command: ACommand) -> bool:
        return command.target_type == self.type and \
               command.value.lower() in ["on", "off"]

    def control_actuator(self, value: str) -> bool:
        if value.lower() == "on":
            self.relay.on()
            self._current_state = "on"
            return True
        elif value.lower() == "off":
            self.relay.off()
            self._current_state = "off"
            return True
        else:
            return False


if __name__ == "__main__":
    relay_pin = 16
    fan_controller = FanController(relay_pin)

    try:
        while True:
            fan_controller.control_actuator("on")
            sleep(2)
            fan_controller.control_actuator("off")
            sleep(2)
    except KeyboardInterrupt:
        print("Fan control interrupted.")
