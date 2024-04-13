from signal import pause
from actuators import IActuator, ACommand
import time


class MockActuator(IActuator):
    _current_state: str
    type: ACommand.Type

    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        self.duration = 0
        self.type = type
        self._current_state = initial_state

    def validate_command(self, command: ACommand) -> bool:
        return command.target_type == self.type

    def control_actuator(self, value: str) -> bool:
        previous_duration = self.duration

        try:
            self.duration = float(value)
        except TypeError:
            print(f"Invalid argument {value}, must be a float")

        print(f"{self.type.name} On")

        time.sleep(float(value))

        print(f"{self.type.name} Off")

        return previous_duration != self.duration


def main():
    actuator = MockActuator(gpio=12)
    duration = 2
    print(f"Controlling {actuator.type.name} for {duration} seconds...")
    actuator.control_actuator(duration)
    print(f"Finished. Press CTRL-C to exit.")
    pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
