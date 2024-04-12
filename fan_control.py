from gpiozero import OutputDevice
from time import sleep
from actuators import IActuator,ACommand

class FanActuator(IActuator):
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str) -> None:
        self.fan = OutputDevice(pin=gpio)
        self.current_state = initial_state

    def validate_command(self, command: ACommand) -> bool:
        if command.target_type == ACommand.Type.FAN:
            return command.value.upper() == "ON" or command.value.upper() == "OFF"
        return False

    def control_actuator(self, value: str) -> bool:
        old_state = self.fan.is_active
        
        if value.upper() == "ON":
            self.fan.on()
        elif value.upper() == "OFF":
            self.fan.off()

        return self.fan.is_active != old_state


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
