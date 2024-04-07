from actuators import ACommand
from fan_actuator import FanActuator
from led_actuator import LEDActuator

class MockFanActuator(FanActuator):
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        self.fan = "Fan"
        self._current_state = initial_state
        self.type = type

    def control_actuator(self, value: str) -> bool:
        previous_state = self._current_state
        try:
            print(f"Changing fan to {int(value)}")
        except (ValueError, TypeError):
            print(f"Invalid argument {value}, must be 0 or 1")
        self._current_state = value
        return previous_state != self._current_state

class MockLEDActuator(LEDActuator):
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        self.led = "LED"
        self._current_state = initial_state
        self.type = type

    def control_actuator(self, value: str) -> bool:
        previous_duration = self._current_state

        try:
            self._current_state = float(value)
        except TypeError:
            print(f"Invalid argument {value}, must be a float")
        if self.type == ACommand.Type.LIGHT_ON_OFF:
            if self._current_state == 1:
                print("LED ON")
            else:
                print("LED OFF")
        else:
            print(f"Pulsing LED twice for {self._current_state/2}")

        return previous_duration != self._current_state