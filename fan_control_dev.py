#!/usr/bin/env python
from gpiozero import OutputDevice
from time import sleep

from actuators import IActuator,ACommand

class FanActuatorDev(IActuator):
    def __init__(self,type: ACommand, initial_state: str = "0") -> None:
        super(IActuator, self).__init__()
        self.current_state = initial_state
        self.type = type

    def validate_command(self,command:ACommand) -> bool:
        return command.value not in (0, 1)



    def control_actuator(self, value: str) -> bool:
        previous_state = self.current_state
        self.current_state = str(value)
        print(f"Fan state: {self.current_state}")
        return previous_state != self.current_state


def main():
    fan_actuator = FanActuatorDev(type=ACommand.Type.FAN)
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
