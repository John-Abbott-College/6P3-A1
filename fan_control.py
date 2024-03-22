from gpiozero import OutputDevice
from time import sleep


class FanActuator:
    def __init__(self, gpio: int, initial_state: str = "0") -> None:
        self.gpio = gpio
        self.current_state = initial_state
        self.fan = OutputDevice(pin=gpio)


    def control_actuator(self, value: str) -> bool:
        previous_state = self.current_state
        try:
            self.fan.value = int(value)
        except (ValueError, TypeError):
            print(f"Invalid argument {value}, must be 0 or 1")
        self.current_state = str(self.fan.value)
        return previous_state != self.current_state


def main():
    fan_actuator = FanActuator(gpio=16)
    fan_actuator.control_actuator("1")
    print(f"Fan state: {fan_actuator.current_state}")
    sleep(2)
    fan_actuator.control_actuator("0")
    print(f"Fan state: {fan_actuator.current_state}")
    sleep(2)


if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        pass