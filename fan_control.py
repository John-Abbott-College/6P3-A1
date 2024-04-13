from gpiozero import OutputDevice
from time import sleep
from actuators import IActuator, ACommand


class FanActuator(IActuator):
    __current_state: str
    type: ACommand.Type

    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        self.gpio = gpio
        self._current_state = initial_state
        self.fan = OutputDevice(pin=gpio)
        self.type = type

    def validate_command(self, command: ACommand) -> bool:
        return command.target_type == self.type

    def control_actuator(self, value: str) -> bool:
        previous_state = self._current_state
        try:
            self.fan.value = int(value)
        except (ValueError, TypeError):
            print(f"Invalid argument {value}, must be 0 or 1")
        self._current_state = str(self.fan.value)
        return previous_state != self._current_state


def main():
    fan_actuator = FanActuator(gpio=16)
    fan_actuator.control_actuator("1")
    print(f"Fan state: {fan_actuator._current_state}")
    sleep(2)
    fan_actuator.control_actuator("0")
    print(f"Fan state: {fan_actuator._current_state}")
    sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
