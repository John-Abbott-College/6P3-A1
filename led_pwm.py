from gpiozero import PWMLED
from signal import pause
from actuators import IActuator, ACommand
import os
from dotenv import load_dotenv

class LEDActuator(IActuator):
    _current_state: str
    type: ACommand.Type

    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        if os.environ['PROD_MODE_ON']:
            self.led = PWMLED(gpio)
        self.duration = 0
        self.type = type
        self._current_state = initial_state

    def validate_command(self, command: ACommand) -> bool:
        return command.target_type == self.type

    def control_actuator(self, value:str) -> bool:
        previous_duration = self.duration

        try:
            self.duration = float(value)
        except TypeError:
            print(f"Invalid argument {value}, must be a float")

        if os.environ['PROD_MODE_ON']:
            self.led.pulse(
                fade_in_time = self.duration/2, 
                fade_out_time = self.duration/2, 
                n = 2, background=False)
        else:
            print('ON')

        return previous_duration != self.duration


def main():
    load_dotenv()
    led = LEDActuator(gpio=12)
    duration = 2
    print(f"LED pulsing twice for {duration} seconds...")
    led.control_actuator(duration)
    print(f"Finished. Press CTRL-C to exit.")
    pause()


if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        pass
