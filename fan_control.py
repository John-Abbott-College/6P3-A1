from gpiozero import OutputDevice
from actuators import IActuator, ACommand

class FanActuator(IActuator):
    def __init__(self, gpio: int, initial_state: str = "0") -> None:
        self._gpio = gpio
        self._current_state = initial_state
        self.type = ACommand.Type.FAN
        self._fan = OutputDevice(pin=gpio)

    def validate_command(self, command: ACommand) -> bool:
        return command.target_type == ACommand.Type.FAN

    def control_actuator(self, value: str) -> bool:
        if value not in ["0", "1"]:
            return False
        self._fan.value = int(value)
        self._current_state = str(self._fan.value)
        return True