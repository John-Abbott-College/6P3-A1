from gpiozero import PWMLED
from signal import pause

from actuators import IActuator, ACommand

class LEDActuator(IActuator):
    def __init__(self, myType: ACommand.Type, gpio:int) -> None:
        self.led = PWMLED(gpio)
        self.type = myType
        self.duration = 0

    def validate_command(self, command: ACommand) -> bool:
        pass

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
    led_onoff = LEDActuator(gpio=12, myType = ACommand.Type.LIGHT_ON_OFF)
    led_pulse = LEDActuator(gpio=12, myType = ACommand.Type.LIGHT_PULSE)
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
