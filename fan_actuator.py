from gpiozero import OutputDevice
from actuators import IActuator, ACommand

class FanActuator(IActuator):
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        self.fan = OutputDevice(gpio)
        self._current_state = initial_state
        self.type = type

    def validate_command(self, command: ACommand) -> bool:
        try:
            value = int(value)
            if value not in [ 0, 1 ]:
                return False
        except (ValueError, TypeError):
            return False

        # Validate the command type
        return command.target_type == self.type

    def control_actuator(self, value: str) -> bool:
        previous_state = self._current_state
        try:
            self.fan.value = int(value)
        except (ValueError, TypeError):
            print(f"Invalid argument {value}, must be 0 or 1")
        self._current_state = str(self.fan.value)
        return previous_state != self._current_state

if __name__ == "__main__":
    import time
    fan = FanActuator(22, ACommand.Type.FAN, "0")
    while True:
        print(fan.control_actuator("0"))
        time.sleep(1)
        print(fan.control_actuator("1"))
        time.sleep(1)
