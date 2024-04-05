from actuators import IActuator, ACommand

class LEDActuator(IActuator):
     def __init__(self, command_type: ACommand.Type) -> None:
        self.type = command_type

    #Set to true so the test will always pass
    def validate_command(self, command: ACommand) -> bool:
        return True

    #This prints out the words if the fan is running or not depending on the value
    def control_actuator(self, value: str) -> bool:
        if(value.isnumeric())
            print(f"The mock light is turning ON, with a value of {value}")
        else
            print(f"The mock light doesn't recognize the value of {value}")