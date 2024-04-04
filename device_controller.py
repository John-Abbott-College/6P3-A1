from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand

from fan_control import FanActuator 
from led_pwm import LEDActuator
from temp_humi_sensor import TempHumiditySensor

class DeviceController:

    def __init__(self) -> None:
        self._sensors: list[ISensor] = self._initialize_sensors()
        self._actuators: list[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list. Intended to be used in class constructor.
        :return List[ISensor]: List of initialized sensors.
        """
        
        return [
            # Instantiate each sensor inside this list, separate items by comma.
            TempHumiditySensor(gpio=26, model="AHT20", command_type=AReading.Type.HUMIDITY),
            
        ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor

        :return list[IActuator]: List of initialized actuators.
        """

        # Instantiate each actuator inside this list, separate items by comma.
        return [
            FanActuator(gpio=16, command_type=ACommand.Type.FAN),
            LEDActuator(gpio=12, command_type=ACommand.Type. LIGHT_PULSE)
        ]

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors. 

        :return list[AReading]: a list containing all readings collected from sensors.
        """
        readings: list[AReading] = []
        for sensor in self._sensors:
            for total_readings in sensor.read_sensor():
                readings.append(total_readings)
                   
        return readings

    def control_actuators(self, commands: list[ACommand]) -> None:
        """Controls actuators according to a list of commands. Each command is applied to it's respective actuator.
        :param list[ACommand] commands: List of commands to be dispatched to corresponding actuators.
        """
        for command in commands:
            for actuator in self._actuators:      
                          
                if actuator.type == command.target_type:
                    print(actuator.validate_command(actuator))
                    print(command.__repr__())
                    actuator.control_actuator(command.value)                    
                    sleep(2)
                   
               
        return
                
                
        



if __name__ == "__main__":
    """This script is intented to be used as a module, however, code below can be used for testing.
    """

    device_manager = DeviceController()

    TEST_SLEEP_TIME = 2

    fan_command_on = ACommand(ACommand.Type.FAN, "1")
    fan_command_off = ACommand(ACommand.Type.FAN, "0")
    led_command = ACommand(ACommand.Type.LIGHT_PULSE, "2")
        
    real_commands = [fan_command_on, fan_command_off, led_command]
    fake_commands = [ACommand(ACommand.Type.FAN, "2"), ACommand(ACommand.Type.LIGHT_ON_OFF, "s")]

    while True:
        temp_reading, humid_reading = device_manager.read_sensors()
        print('Temperature in Celsius is {:.2f} C'.format(temp_reading))
        print('Relative Humidity is {:.2f} %'.format( humid_reading))
        device_manager.control_actuators(real_commands)
        #device_manager.control_actuators(fake_commands)

        sleep(TEST_SLEEP_TIME)
