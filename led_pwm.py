from gpiozero import PWMLED
from signal import pause
from actuators import IActuator, ACommand

#TEST TEST TEST

class LEDActuator(IActuator):
    def __init__(self, gpio:int,command_type: ACommand.Type) -> None:
        self.led = PWMLED(gpio)
        self.type = command_type
        self.duration = 0

    #Borrowed this validation code from programming 4 last year, where we compare to make 
    #sure valid types are passed in
    #Got the idea for command.value.isnumeric() from here: https://www.tutorialsteacher.com/python/string-isnumeric
    def validate_command(self, command: ACommand) -> bool:
        return (command.target_type == self.type) and command.value.isnumeric()

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
    led = LEDActuator(gpio=12, command_type=ACommand.Type.LIGHT_PULSE)
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
