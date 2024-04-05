from gpiozero import PWMLED
from actuators import IActuator, ACommand

class LEDActuator(IActuator):
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        self.led = PWMLED(gpio)
        self._current_state = initial_state
        self.type = type

    def validate_command(self, command: ACommand) -> bool:
        # Validate the value is a float greater than 0.
        try:
            value = float(command.value)
            if value < 0:
                return False
        except TypeError:
            return False

        # Validate the command type
        return command.target_type == self.type

    def control_actuator(self, value: str) -> bool:
        previous_duration = self._current_state

        try:
            self._current_state = float(value)
        except TypeError:
            print(f"Invalid argument {value}, must be a float")

        self.led.pulse(
            fade_in_time = self._current_state/2, 
            fade_out_time = self._current_state/2, 
            n = 2, background=False)

        return previous_duration != self._current_state

if __name__ == "__main__":
    led = LEDActuator(5, ACommand.Type.LIGHT_PULSE, "0")
    while True:
        print(led.control_actuator("2"))
