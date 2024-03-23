#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
from typing import Literal, Union
from actuators import IActuator, ACommand

FAN_GPIO_PIN = 22


class FanController():
    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str = "off") -> None:
        """
        Initialize the Fan controller and sets the GPIO mode.

        Args:
        - gpio: The GPIO pin connected to the fan.
        - type: The type of command this actuator responds to (should be FAN).
        - initial_state: The initial state of the fan ("on" or "off").
        """
        self._current_state = GPIO.LOW if initial_state.lower() == "off" else GPIO.HIGH
        print(self._current_state)
        self.type = type
        self.gpio_pin = gpio

        # Set the GPIO mode
        GPIO.setmode(GPIO.BCM)
        # Set the GPIO pin as output
        GPIO.setup(self.gpio_pin, GPIO.OUT)
        GPIO.output(self.gpio_pin, self._current_state)


    def validate_command(self, command: ACommand) -> bool:
        """Validates that a command can be used with the fan actuator.

        Args:
            command (ACommand): The command to be validated.

        Returns:
            bool: True if the command is compatible, false otherwise.
        """

        return command.target_type == self.type and type(command.value) is str and (command.value.lower() == "on" or command.value.lower() == "off")

    def control_actuator(self, value: str) -> bool:
        """
        Controls the fan's state.

        Args:
        - value (str): The new state of the fan, "on" or "off".

        Returns:
        bool: True if the fan state changes, otherwise False.
        """
        if value.lower() == "on":
            if self._current_state == GPIO.LOW:
                GPIO.output(self.gpio_pin, GPIO.HIGH)
                self._current_state = GPIO.HIGH
                return True
        elif value.lower() == "off":
            if self._current_state == GPIO.HIGH:
                GPIO.output(self.gpio_pin, GPIO.LOW)
                self._current_state = GPIO.LOW
                return True
            
            return False
    
    def clean_up(self):
        """Cleans up the device"""
        GPIO.cleanup()


if __name__ == "__main__":
    fan_controller = FanController(gpio=FAN_GPIO_PIN, type=ACommand.Type.FAN, initial_state="off")
    print(fan_controller.control_actuator("on"))
    print(fan_controller.control_actuator("off"))
    print(fan_controller.control_actuator("off"))
    try:
        while True:
            fan_controller.control_actuator("on")
            time.sleep(2)
            fan_controller.control_actuator("off")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Program interrupted. Cleaning up GPIO...")
        fan_controller.clean_up()