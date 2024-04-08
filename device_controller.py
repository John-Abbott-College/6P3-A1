from sensors import ISensor, AReading
from time import sleep
from actuators import IActuator, ACommand
from fan_control import FanActuator
from led_pwm import LEDActuator
from temp_humi_sensor import TempHumiditySensor
from dotenv import load_dotenv
import os
from mock import MockDeviceController

class DeviceController:
    def __init__(self) -> None:
        load_dotenv()
        environment = os.getenv("ENVIRONMENT")
        if environment == "development":
            print("dev")
            self.device = MockDeviceController()
            self.device.run()
        elif environment == "production":
            print("prod")
            self._sensors: list[ISensor] = self._initialize_sensors()
            self._actuators: list[IActuator] = self._initialize_actuators()
        else:
            raise ValueError("Invalid environment mode specified in .env file")

    def _initialize_sensors(self) -> list[ISensor]:
        """Initializes all sensors and returns them as a list. Intended to be used in class constructor."""
        return [
            TempHumiditySensor(address=0x38, bus=4)
        ]

    def _initialize_actuators(self) -> list[IActuator]:
        """Initializes all actuators and returns them as a list. Intended to be used in class constructor."""
        return [
            LEDActuator(gpio=12),
            FanActuator(gpio=16)
        ]

    def read_sensors(self) -> list[AReading]:
        """Reads data from all initialized sensors.

        :return list[AReading]: a list containing all readings collected from sensors.
        """
        readings: list[AReading] = []
        for sensor in self._sensors:
            readings.extend(sensor.read_sensor())
        return readings

    def run_in_development_mode(self):
        """Runs the device in development mode."""
        while True:
            self.actuator.turn_on()
            sleep(2)
            self.actuator.turn_off()
            sleep(2)

    def control_actuators(self) -> None:
        """Controls actuators according to a list of commands."""
        for actuator in self._actuators:
            if isinstance(actuator, FanActuator):
                actuator.control_actuator("1" if actuator.current_state == "0" else "0")
            elif isinstance(actuator, LEDActuator):
                actuator.led.pulse(fade_in_time=1, fade_out_time=1, n=1, background=False)
                sleep(2) 
                pass

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
