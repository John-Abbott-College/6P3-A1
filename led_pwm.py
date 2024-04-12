from gpiozero import PWMLED
from signal import pause
from actuators import IActuator, ACommand 

class LEDActuator(IActuator):
    def __init__(self, gpio:int, type: ACommand) -> None:
        self.gpio = gpio
        self._current_state = "0"
        self.type = type
        self.led = PWMLED(gpio)
        self.duration = 0

    def validate_command(self, command: ACommand) -> bool:
        return command == self.type

    def control_actuator(self, value:str) -> bool:
        previous_duration = self.duration

        try:
            self.duration = float(value)
        except TypeError:
            print(f"Invalid argument {value}, must be a float")

        self.led.pulse(
            fade_in_time = self.duration/2, 
            fade_out_time = self.duration/2, 
            n = 2, background=False)

        return previous_duration != self.duration

