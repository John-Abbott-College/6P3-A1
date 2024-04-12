from actuators import IActuator, ACommand

class MockFanActuator(IActuator):
    def __init__(self, gpio: int, type: ACommand, initial_state: str = "0") -> None:
        self.gpio = gpio
        self._current_state = initial_state
        self.type = type

    def validate_command(self, command: ACommand) -> bool:
        return command == self.type

    def control_actuator(self, value: str) -> bool:
        print(f"Mock Fan Actuator - Setting fan state to: {value}")
        previous_state = self._current_state
        self._current_state = value
        return previous_state != self._current_state

def main():
    fan_actuator = MockFanActuator(gpio=16, type=ACommand)
    fan_actuator.control_actuator("1")
    print(f"Fan state: {fan_actuator._current_state}")
    fan_actuator.control_actuator("0")
    print(f"Fan state: {fan_actuator._current_state}")

if __name__ == "__main__":
    main()
