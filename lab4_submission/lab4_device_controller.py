#!/usr/bin/env python3

from fan_control import FanController, FAN_GPIO_PIN
from led_pwm import LEDController, LED_GPIO_PIN
from temp_humi_sensor import TemperatureHumiditySensor, AHT20_ADDRESS, BUS
from typing import Literal, Union, Any
import time


class HardwareController():
    def __init__(self, 
                 fan_GPIO_pin: Union[int, str] = FAN_GPIO_PIN, 
                 LED_GPIO_pin: Union[int, str] = LED_GPIO_PIN, 
                 sensor_address: int = AHT20_ADDRESS,
                 sensor_bus: Union[Any, Literal[0, 1]] = BUS
                 ) -> None:
        """
            Initialize the Hardware Controller and instantiates all hardware devices.

            Args:
            - fan_GPIO_pin:The GPIO pin connected to the relay.
            - LED_GPIO_pin: The GPIO pin (BCM mode) connected to the LED.
            - sensor_address: The address of the sensor.
            - sensor_bus: The i2c bus the sensor is connected to.
        """

        self.fanController = FanController(fan_GPIO_pin)
        self.ledController = LEDController(LED_GPIO_pin)
        self.temperatureHumiditySensor = TemperatureHumiditySensor(address= sensor_address, 
                                                                   bus = sensor_bus)
    
    def control_actuators(self) -> None:
        """
            Changes the state of all actuators.
        """
        self.fanController.control_actuator(True)
        self.ledController.control_actuator(2)
        time.sleep(0.9)
        self.fanController.control_actuator(False)
        time.sleep(1.1)


    def clean_up_actuators(self) -> None:
        """
            Cleans up the actuators.
        """
        print("\nCleaning up!...")
        self.ledController.clean_up()
        self.fanController.clean_up()

    def read_sensors(self) -> None:
        """
            Prints a list of the latest readings from all sensors.
        """
        readings = self.temperatureHumiditySensor.read_sensor()
        for reading in readings:
            print(reading)

    def loop(self) -> None:
        """
            Reads all sensors and controls actuators every 2 seconds.
        """
        try:
            while True:
                self.read_sensors()
                self.control_actuators()
        except KeyboardInterrupt:
            self.clean_up_actuators()


if __name__ == "__main__":
    hc = HardwareController()
    hc.loop()
