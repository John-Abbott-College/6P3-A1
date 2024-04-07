from gpiozero import OutputDevice
from time import sleep
from actuators import IActuator, ACommand

class MockFanController(IActuator):

    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str):
        self.gpio = gpio
        self.type = type
        self.current_state = initial_state
        self.fan = f"Mock fan using pin {gpio}"

    def control_actuator(self, value):
        if value.upper() == "ON":
            self.current_state = value.upper()
        elif value.upper() == "OFF":
            self.current_state = value.upper()
        else:
            print(f"The command {value} is an invalid command. Please provide 'ON' or 'OFF'")

    def validate_command(self, command):
        if command.target_type == ACommand.Type.FAN and (command.value.upper() == "ON" or command.value.upper() == "OFF"):
            return True
        return False


if __name__ == "__main__":
    fan = MockFanController(16, ACommand.Type.FAN, "OFF")
    try: 
        fan.control_actuator("ON")
        sleep(2)
        fan.control_actuator("OFF")
        sleep(2)
    except KeyboardInterrupt:
        pass

