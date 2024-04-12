from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand
from led_pwm import LEDActuator
from fan_control import FanActuator
from temp_humi_sensor import TempHumiditySensor
from dotenv import load_dotenv
import os

class DeviceController:
    def __init__(self) -> None:
        self._sensors = [TempHumiditySensor(address=0x38, bus=4)]
        self._actuators = [
            LEDActuator(gpio=12),
            FanActuator(gpio=16)
        ]

    def read_sensors(self):
        """Read data from all initialized sensors."""
        return [sensor.read_sensor() for sensor in self._sensors]

    def control_actuators(self, commands):
        """Control actuators based on commands from the dashboard."""
        for command in commands:
            if command.target_type == ACommand.Type.LIGHT_PULSE:
                # Extract LED value from command and convert to int
                led_value = int(command.value)
                if led_value == 1:
                    self._actuators[0].turn_on()
                else:
                    self._actuators[0].turn_off()
            elif command.target_type == ACommand.Type.FAN:
                # Turn fan actuator on or off based on the command value
                fan_value = int(command.value)
                if fan_value == 1:
                    self._actuators[1].turn_on_fan()
                else:
                    self._actuators[1].turn_off_fan()

        
    def loop(self) -> None:
        """Main loop of the device controller."""
        while True:
            self.control_actuators()
            print(self.read_sensors())
            sleep(2)

class MockSensor:
    def __init__(self, name):
        self.name = name

    def read(self):
        print(f"Reading from {self.name} sensor")

class MockActuator:
    def __init__(self, name):
        self.name = name

    def turn_on(self):
        print(f"Turning {self.name} actuator ON")

    def turn_off(self):
        print(f"Turning {self.name} actuator OFF")

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors."""
        readings: list[AReading] = []
        for sensor in self._sensors:
            readings.extend(sensor.read_sensor())
        return readings

if __name__ == "__main__":
    device_controller = DeviceController()
    try:
        device_controller.loop()
    except KeyboardInterrupt:
        pass