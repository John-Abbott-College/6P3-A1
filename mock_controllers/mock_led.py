from actuators import IActuator, ACommand

class MockLEDActuator(IActuator):
    def __init__(self, gpio:int, type: ACommand) -> None:
        self.gpio = gpio
        self._current_state = "0"
        self.type = type
        self.duration = 0

    def validate_command(self, command: ACommand) -> bool:
        return command == self.type

    def control_actuator(self, value:str) -> bool:
        print(f"Mock LED Actuator - Setting LED duration to: {value} seconds")
        previous_duration = self.duration

        try:
            self.duration = float(value)
        except TypeError:
            print(f"Invalid argument {value}, must be a float")

        return previous_duration != self.duration

# Test the mock LED actuator
def main():
    led_actuator = MockLEDActuator(gpio=12, type=ACommand)
    duration = 2
    print(f"LED pulsing twice for {duration} seconds...")
    led_actuator.control_actuator(duration)
    print(f"Finished. Press CTRL-C to exit.")

if __name__ == "__main__":
    main()
