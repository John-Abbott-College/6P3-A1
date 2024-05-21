from gpiozero import OutputDevice
from time import sleep
from actuators import IActuator, ACommand


class FanActuator(IActuator):
    def __init__(self, gpio: int, type:ACommand.Type, initial_state: str = "0") -> None:
        self.gpio = gpio
        self.current_state = initial_state
        self.fan = OutputDevice(pin=gpio)
        self.type = type

    def validate_command(self, command: ACommand) -> bool:
        return command.target_type == self.type

    def control_actuator(self, value: str) -> bool:
        previous_state = self.current_state
        try:
            self.fan.value = int(value)
        except (ValueError, TypeError):
            print(f"Invalid argument {value}, must be 0 or 1")
        self.current_state = str(self.fan.value)
        return previous_state != self.current_state