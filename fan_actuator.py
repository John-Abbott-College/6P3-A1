from gpiozero import OutputDevice
from actuators import IActuator, ACommand

class FanActuator(IActuator):
    @IActuator.__init__
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        self.fan = OutputDevice(gpio)
        self._current_state = initial_state
        self.type = type

    # Validates that a command can be used with the specific actuator.
    @IActuator.validate_command
    def validate_command(self, command: ACommand) -> bool:
        try:
            value = int(value)
            if value not in [ 0, 1 ]:
                return False
        except (ValueError, TypeError):
            return False

        # Validate the command type
        return command.target_type == self.type

    # Sets the actuator to the value passed as argument.
    @IActuator.control_actuator
    def control_actuator(self, value: str) -> bool:
        previous_state = self.current_state
        try:
            self.fan.value = int(value)
        except (ValueError, TypeError):
            print(f"Invalid argument {value}, must be 0 or 1")
        self.current_state = str(self.fan.value)
        return previous_state != self.current_state

