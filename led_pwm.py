from gpiozero import PWMLED
from signal import pause
from time import sleep
from actuators import IActuator, ACommand

class LEDActuator(IActuator):

    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        self.led = PWMLED(gpio)
        self.duration = initial_state
        self.type = type

    def validate_command(self, command: ACommand) -> bool:
        try:
            int(command.value)
            return True
        except:
            return False

    

    def control_actuator(self, value:str) -> bool:
        previous_duration = self.duration

        try:
            if self.validate_command(ACommand(self.type, value)):
                self.duration = float(value)
            else:
                raise Exception
        except TypeError:
            print(f"Invalid argument {value}, must be a float")

        if self.type == ACommand.Type.LIGHT_PULSE:
            self.led.pulse(
            fade_in_time = self.duration/2, 
            fade_out_time = self.duration/2, 
            n = 2, background=False)
        else:
            self.led.on()
            sleep(self.duration/2)
            self.led.off()
            sleep(self.duration/2)

        

        return previous_duration != self.duration


def main():
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
