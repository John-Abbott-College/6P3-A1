from gpiozero import PWMLED
from actuators import IActuator, ACommand

class LEDController(IActuator):

    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str):
        self.gpio = gpio
        self.type = type
        self.current_state = initial_state
        self.led = PWMLED(gpio)
        self.control_actuator(initial_state)

    def control_actuator(self, value):
        if self.type == ACommand.Type.LIGHT_ON_OFF:
            self.on_off_mode(value)
        elif self.type == ACommand.Type.LIGHT_PULSE:
            self.pulse_mode(value)
        else:
            print(f"LED type {self.type} is invalid")

    def validate_command(self, command):
        if command.target_type == ACommand.Type.LIGHT_ON_OFF or command.target_type == ACommand.Type.LIGHT_PULSE:
            if command.value.upper() == "ON" or command.value.upper() == "OFF":
                return True
        return False

    def pulse_mode(self, value):
        if value.upper() == "ON":
            self.led.pulse()
        elif value.upper() == "OFF":
            self.led.off()
        else:
            print(f"The command {value} is an invalid command. Please provide 'ON' or 'OFF'")

    def on_off_mode(self, value):
        if value.upper() == "ON":
            self.led.on()
        elif value.upper() == "OFF":
            self.led.off()
        else:
            print(f"The command {value} is an invalid command. Please provide 'ON' or 'OFF'")


if __name__ == "__main__":
    led = LEDController(18, ACommand.Type.LIGHT_ON_OFF, "ON")
    while True:
        print(f"LED State {led.current_state}")

