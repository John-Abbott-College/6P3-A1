from gpiozero import PWMLED
from time import sleep

class LEDController:
    def __init__(self, pin: int) -> None:
        self.led = PWMLED(pin)
        self._pulse_duration = 0

    def pulse(self, duration: int) -> None:
        self.led.pulse(duration, duration)
        sleep(duration * 2)

    def control_actuator(self, duration: int) -> bool:
        # Pulse the LED twice.
        self.pulse(duration)
        self.pulse(duration)

        ret = self._pulse_duration != duration
        self._pulse_duration = duration
        return ret

if __name__ == "__main__":
    led = LEDController(5)
    led.control_actuator(3)