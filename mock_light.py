from gpiozero import PWMLED
from signal import pause
from time import sleep
from actuators import ACommand, IActuator
from led_pwm import LEDActuator


class MockLEDActuator(LEDActuator):
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str = "OFF") -> None:
        """Constructor for Actuator class. Must define interface's class properties

        :param ACommand.Type type: Type of command the actuator can respond to.
        :param str initial_state: initializes 'current_state' property of a new actuator.
        If not passed, actuator implementation is responsible for setting a default value.
        """
        self._current_state = initial_state
        self.type = type
        self.duration = 0

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
        if (self.type == ACommand.Type.LIGHT_ON_OFF):
            if(value == "ON"):
                previous_state = self._current_state
                self._current_state = "ON"
                print("Light is " + self._current_state)
                return previous_state != self._current_state
            elif (value == "OFF"):
                previous_state = self._current_state
                self._current_state = "OFF"
                print("Light is " + self._current_state)
                return previous_state != self._current_state
        else:
            previous_duration = self.duration

            try:
                self.duration = float(value)
            except TypeError:
                print(f"Invalid argument {value}, must be a float")

            if(self.duration != 0):
                self._current_state = "PULSE"
                print("Pulse light is " + self._current_state)
                sleep(self.duration)
            
            self._current_state = "OFF"
            print("Pulse light is " + self._current_state)

            return previous_duration != self.duration
        

def main():
    
    led = MockLEDActuator(12, ACommand.Type.LIGHT_PULSE, "ON")
    duration = 2
    print(f"LED pulsing twice for {duration} seconds...")
    led.control_actuator(duration)
    print(f"Finished. Press CTRL-C to exit.")
    pause()

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        pass