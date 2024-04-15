from gpiozero import OutputDevice
from time import sleep
from actuators import IActuator, ACommand

class FanActuator(IActuator):
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str = "0") -> None:
        self.gpio = gpio
        self.type = type
        self.current_state = initial_state
        self.fan = OutputDevice(pin=gpio)

        self._state_values_dict:dict[str, list[str]] = {
            "on": ["true","1","high","on"],
            "off": ["false","0","low","off"]
        }

    def validate_command(self, command: ACommand) -> bool:
        return command.target_type == self.type 


    def control_actuator(self, value: str) -> bool:
        previous_state = self.current_state
        if self.validate_command(ACommand(ACommand.Type.FAN,value)):

            if value.lower() in self._state_values_dict["on"]:
                self.fan.on()
            elif value.lower() in self._state_values_dict["off"]:
                self.fan.off()

        else:
            print(f"Invalid argument {value}, must be one of {', '.join(self._state_values_dict['on'])} or {', '.join(self._state_values_dict['off'])}")
            return False


def main():
    fan_actuator = FanActuator(gpio=16, type=ACommand.Type.FAN)
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
