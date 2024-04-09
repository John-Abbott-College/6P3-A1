from gpiozero import PWMLED
from signal import pause
from actuators import IActuator, ACommand

class LEDActuator(IActuator):
    
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str = "0") -> None:
        self.gpio = gpio
        self.type = type
        self.current_state = initial_state
        self.led = PWMLED(gpio)
        self.duration = 0

    def validate_command(self, command: ACommand) -> bool:
        try:
            int(command.value)
            return True
        except:
            return False

    def control_actuator(self, value: str) -> bool:
        previous_duration = self.duration

        try:
            if self.validate_command(ACommand(self.Type,value)):
                self.duration = float(value)
        except TypeError:
            print(f"Invalid argument {value}, must be a float")

        if self.type == ACommand.Type.LIGHT_PULSE:
            self.led.pulse(
                fade_in_time=self.duration / 2,
                fade_out_time=self.duration / 2,
                n=2, background=False)
        else:
            self.led.on()
            sleep(self.duration/2)
            self.led.off()
            sleep(self.duration/2)


        return previous_duration != self.duration


