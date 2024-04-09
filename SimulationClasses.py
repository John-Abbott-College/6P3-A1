from time import sleep
from sensors import AReading, ISensor
from actuators import IActuator, ACommand
import random


class DevSimulationTempHumSensor(ISensor):
    def __init__(self) -> None:
        pass

    def read_sensor(self) -> list[AReading]:
        temp, hum = (random.randint(-20, 40), random.randint(10, 80))

        return [AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, temp), AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, hum)]


class DevFanActuation(IActuator):
    def __init__(self, type: ACommand.Type, initial_state: str = "0") -> None:
        self.current_state = initial_state
        self.type = type


    def validate_command(self, command: ACommand) -> bool:
        return command.value == "0" or command.value == "1"
    
    
    def control_actuator(self, value: str) -> bool:
        previous_state = self.current_state
        try:
            if self.validate_command(ACommand(ACommand.Type.FAN, value)):
                if value == "0":
                    print("Fan: OFF")
                else:
                    print("Fan: ON")
            else:
                raise Exception
        except (ValueError, TypeError):
            print(f"Invalid argument {value}, must be 0 or 1")
        self.current_state = str(value)
        return previous_state != self.current_state

class DevLEDActuation(IActuator):

    def __init__(self, type: ACommand.Type, initial_state: str) -> None:
        self.duration = initial_state
        self.type = type
        print(self.type)

    def validate_command(self, command: ACommand) -> bool:
        try:
            int(command.value)
            return True
        except:
            return False

    def control_actuator(self, value:str) -> bool:
        previous_duration = self.duration

        try:
            if self.validate_command(ACommand(self.type, value)):
                self.duration = float(value)
            else:
                raise Exception
        except TypeError:
            print(f"Invalid argument {value}, must be a float")

        if self.type == ACommand.Type.LIGHT_PULSE:
            print("pulse")
            print("Led: ON")
            sleep(self.duration/2)
            print("Led: OFF")
            sleep(self.duration/2)
            print("Led: ON")
            sleep(self.duration/2)
            print("Led: OFF")
            sleep(self.duration/2)
        else:
            print("on/off")
            print("Led: ON")
            sleep(self.duration/2)
            print("Led: OFF")
            sleep(self.duration/2)

        

        return previous_duration != self.duration
  


