from gpiozero import OutputDevice
from time import sleep
from actuators import IActuator, ACommand
from fan_control import FanActuator

class MockFanActuator(FanActuator):
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str = "OFF") -> None:
        """Constructor for Actuator class. Must define interface's class properties

        :param ACommand.Type type: Type of command the actuator can respond to.
        :param str initial_state: initializes 'current_state' property of a new actuator.
        If not passed, actuator implementation is responsible for setting a default value.
        """

        # can be ON or OFF
        self._current_state = initial_state
        self.type = type

    def validate_command(self, command: ACommand) -> bool:
        """Validates that a command can be used with the specific actuator.

        :param ACommand command: the command to be validated.
        :return bool: True if command can be consumed by the actuator.
        """
        if(command.target_type == self.type):
            return True
        return False
    
    def control_actuator(self, value: str) -> bool:
        """Sets the actuator to the value passed as argument.

        :param str value: Value used to set the new state of the actuator. Value is parsed inside concrete classes.
        :return bool: True if the state of the actuator changed, false otherwise.
        """
        if(value == "ON"):
            previous_state = self._current_state
            self._current_state = "ON"
            print("Fan is turned " + self._current_state)
            return previous_state != self._current_state
        elif (value == "OFF"):
            previous_state = self._current_state
            self._current_state = "OFF"
            print("Fan is turned " + self._current_state)
            return previous_state != self._current_state
        else:
            print(f"Invalid argument {value}, must be ON or OFF")
            return False
        

def main():
    fan_actuator = MockFanActuator(16, ACommand.Type.FAN, "OFF")
    sleep(2)
    fan_actuator.control_actuator("ON")
    print(f"Fan state: {fan_actuator._current_state}")
    sleep(2)
    fan_actuator.control_actuator("OFF")
    print(f"Fan state: {fan_actuator._current_state}")
    sleep(2)


if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        pass