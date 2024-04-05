from gpiozero import PWMLED
from signal import pause
from actuators import IActuator,ACommand


class LEDActuator(IActuator):
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        self.led = PWMLED(gpio)
        self.type = type
        self.control_actuator(initial_state)
        self.duration = 0

    def validate_command(self, command: ACommand) -> bool:
        if command.target_type == ACommand.Type.LIGHT_ON_OFF or command.target_type == ACommand.Type.LIGHT_ON_OFF :
            return command.value.upper() == "ON" or command.value.upper() == "OFF" 
        return False

    def control_actuator(self, value: str) -> bool:
        previous_state= self.led.is_active

        if self.type == ACommand.Type.LIGHT_PULSE:
            print(value)
            if value.isnumeric():
                print("in")
                self.led.pulse(float(value))
            else:
                print("out")
                return False
        elif self.type == ACommand.Type.LIGHT_ON_OFF:
            if value.upper() == "ON":
                self.led.on()
            elif value.upper() == "OFF":
                self.led.off()
        return previous_state != self.led.is_active


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
