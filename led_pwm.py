from gpiozero import PWMLED
from signal import pause
from actuators import IActuator,ACommand

class LEDActuator(IActuator):
    def __init__(self, gpio:int, type:ACommand.Type, initial_state: str = "0") -> None:
        self.led = PWMLED(gpio)
        self.duration = 0

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


def main():
    led = LEDActuator(gpio=12,type=ACommand.Type.LIGHT_PULSE)
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
