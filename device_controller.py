from actuators import IActuator, ACommand, FanController
from typing import List, Union
from sensors import ISensor, HumiditySensor
from time import sleep
from sensors import AReading

class DeviceController:
    def __init__(self) -> None:
        self._sensors: List[ISensor] = self._initialize_sensors()
        self._actuators: List[IActuator] = self._initialize_actuators()

    def _initialize_sensors(self) -> List[ISensor]:
        return [
        HumiditySensor(gpio=0, model="dummy_model", type=AReading.Type.HUMIDITY)
    ]


    def _initialize_actuators(self) -> List[IActuator]:
        return [
            FanController(relay_pin=16),
        ]

    def read_sensors(self, unit: AReading.Unit) -> List[Union[tuple, None]]:
        readings: List[Union[tuple, None]] = []
        for sensor in self._sensors:
            reading = sensor.read_sensor(unit)
            if reading is not None:
                readings.append(reading)
        return readings

    def control_actuators(self, commands: List[ACommand]) -> None:
        for command in commands:
            for actuator in self._actuators:
                if actuator.validate_command(command):
                    actuator.control_actuator(command.value)
                    break
            else:
                print(f"No matching actuator found for command: {command}")

if __name__ == "__main__":
    device_manager = DeviceController()

    TEST_SLEEP_TIME = 2

    while True:

        print("Readings in Celsius:")
        print(device_manager.read_sensors(AReading.Unit.CELCIUS))


        print("Readings in Fahrenheit:")
        print(device_manager.read_sensors(AReading.Unit.FAHRENHEIT))
        
        start_fan_command = ACommand(ACommand.Type.FAN, "on")
        device_manager.control_actuators([start_fan_command])

        sleep(TEST_SLEEP_TIME)
