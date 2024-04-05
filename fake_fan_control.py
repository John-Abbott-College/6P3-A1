from actuators import IActuator, ACommand

class FakeFanActuator(IActuator):
    def __init__(self, command_type: ACommand.Type) -> None:
        self.type = command_type

    
    def validate_command(self, command: ACommand) -> bool:
        return True

    #This prints out the words if the fan is running or not depending on the value
    def control_actuator(self, value: str) -> bool:
        if(value=="1"):
            print(f"The fake fan is turning ON")
        elif(value=="0"):
            print(f"The fake fan is turning OFF")
        else:
            print(f"The fake fan doesn't recognize the value of {value}")