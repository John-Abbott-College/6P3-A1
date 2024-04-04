from gpiozero import PWMLED
from actuators import IActuator, ACommand

class LEDActuator(IActuator):
    @IActuator.__init__
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        self._fan = PWMLED(gpio)
        self._current_state = initial_state
        self.type = type

    # Validates that a command can be used with the specific actuator.
    @IActuator.validate_command
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

    # Sets the actuator to the value passed as argument.
    @IActuator.control_actuator
    def control_actuator(self, value: str) -> bool:
        previous_duration = self.duration

        try:
            self.duration = float(value)
        except TypeError:
            print(f"Invalid argument {value}, must be a float")

        # TODO: What does background do?
        self.led.pulse(
            fade_in_time = self.duration/2, 
            fade_out_time = self.duration/2, 
            n = 2, background=False)

        return previous_duration != self.duration
