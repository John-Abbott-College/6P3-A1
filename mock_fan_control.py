from actuators import IActuator, ACommand

class MockFanActuator(IActuator):
     def __init__(self, command_type: ACommand.Type) -> None:
        self.type = command_type

    #Set to true so the test will always pass
    def validate_command(self, command: ACommand) -> bool:
        return True

    #This prints out the words if the fan is running or not depending on the value
    def control_actuator(self, value: str) -> bool:
        if(value=="1")
            print(f"The mock fan is turning ON")
        elif(value=="0")
            print(f"The mock fan is turning OFF")
        else
            print(f"The mock fan doesn't recognize the value of {value}")