from gpiozero import PWMLED
from actuators import IActuator, ACommand

class LEDActuator(IActuator):
    def __init__(self, gpio: int) -> None:
        self._gpio = gpio
        self.type = ACommand.Type.LIGHT_PULSE
        self._led = PWMLED(gpio)
        self._current_state = "0"

    def validate_command(self, command: ACommand) -> bool:
        return command.target_type == ACommand.Type.LIGHT_PULSE

    def control_actuator(self, value: str) -> bool:
        try:
            duration = float(value)
            self._led.pulse(
                fade_in_time=duration/2, 
                fade_out_time=duration/2, 
                n=1, 
                background=False
            )
            self._current_state = "1"
            return True
        except ValueError:
            return False
