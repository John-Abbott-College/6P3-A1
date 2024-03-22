#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from typing import Literal, Union

FAN_GPIO_PIN = 22


class FanController:
    def __init__(self, pin: Union[int, str]) -> None:
        """
        Initialize the Fan controller and sets the GPIO mode.

        Args:
        - pin: The GPIO pin connected to the relay.
        """
        self.fan_state = GPIO.LOW
        self.gpio_pin = pin

        # Set the GPIO mode
        GPIO.setmode(GPIO.BCM)
        # Set the GPIO pin as output
        GPIO.setup(self.gpio_pin, GPIO.OUT)

    def control_actuator(self, new_state: bool) -> bool:
        """
        Controls the fan's state.

        Args:
        - new_state (bool): The new state of the fan, True for on, false for off.

        Returns:
        bool: True if the fan state changes, otherwise False.
        """
        if new_state:
            if self.fan_state == GPIO.LOW:
                GPIO.output(self.gpio_pin, GPIO.HIGH)
                self.fan_state = GPIO.HIGH
                return True
        else:
            if self.fan_state == GPIO.HIGH:
                GPIO.output(self.gpio_pin, GPIO.LOW)
                self.fan_state = GPIO.LOW
                return True
        return False
    
    def clean_up(self):
        """Cleans up the device"""
        GPIO.cleanup()


if __name__ == "__main__":
    fan_controller = FanController(FAN_GPIO_PIN)
    print(fan_controller.control_actuator(True))
    print(fan_controller.control_actuator(False))
    print(fan_controller.control_actuator(False))
    try:
        while True:
            fan_controller.control_actuator(True)
            time.sleep(2)
            fan_controller.control_actuator(False)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Program interrupted. Cleaning up GPIO...")
        fan_controller.clean_up()