from gpiozero import PWMLED
from signal import pause
from actuators import IActuator, ACommand

class LEDActuator:
    def __init__(self, gpio:int) -> None:
        self.led = PWMLED(gpio)
        self.duration = 0

    def control_actuator(self, value:str) -> bool:
        try:
            brightness = float(value)
        except TypeError:
            print(f"Invalid argument {value}, must be a float")
            return False

        # Set LED brightness to the specified value
        self.led.value = brightness

        return True
    
    def turn_on(self):
        self.led.value = 1.0

    def turn_off(self):
        self.led.value = 0.0


def main():
    led = LEDActuator(gpio=12)
    brightness = 1  # Set brightness to maximum (LED fully on)
    print(f"LED turned on at maximum brightness...")
    led.control_actuator(brightness)
    print(f"Finished. Press CTRL-C to exit.")
    pause()


if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        pass
