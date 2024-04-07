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
            if command.target_type == ACommand.Type.LIGHT_ON_OFF:
                if value not in [0, 1]:
                    return False
            elif command.target_type == ACommand.Type.LIGHT_PULSE:
                if value < 0:
                    return False
            else:
                return False
        except TypeError:
            return False

        return True

    def control_actuator(self, value: str) -> bool:
        previous_duration = self._current_state

        try:
            self._current_state = float(value)
        except TypeError:
            print(f"Invalid argument {value}, must be a float")
        if self.type == ACommand.Type.LIGHT_ON_OFF:
            if self._current_state == 1:
                self.led.on()
            else:
                self.led.off()
        else:
            self.led.pulse(
                fade_in_time = self._current_state/2, 
                fade_out_time = self._current_state/2, 
                n = 2, background=True)

        return previous_duration != self._current_state

if __name__ == "__main__":
    led = LEDActuator(5, ACommand.Type.LIGHT_PULSE, "0")
    while True:
        print(led.control_actuator("1"))
