#!/usr/bin/env python3

from gpiozero import PWMLED
from time import sleep
from typing import Union

LED_GPIO_PIN = 12

class LEDController:
    def __init__(self, pin: Union[int, str]) -> None:
        """
        Initialize the LED controller.

        Args:
        - pin: The GPIO pin (BCM mode) connected to the LED.
        """
        self.led = PWMLED(pin)
    
    def control_actuator(self, pulse_duration: float) -> bool:
        """
        Control the LED to pulse with a specified duration for fading in and out.

        Args:
        - pulse_duration: The duration of the pulse from zero to full brightness and back to zero, in seconds.

        Returns:
        - True if the pulse time is set to a new pulse duration, otherwise False.
        """
        if pulse_duration <= 0:
            return False  # Invalid pulse duration

        # Set the LED to pulse with specified fade in and out times
        self.led.pulse(fade_in_time=pulse_duration/2, 
                       fade_out_time=pulse_duration/2,
                       n=2,
                       background=True)
        
        return True
    
    def clean_up(self):
        """Cleans up the device"""
        self.led.off()

if __name__ == "__main__":
    led_controller = LEDController(LED_GPIO_PIN) 
    try:
        while True:
            led_controller.control_actuator(2)
            sleep(2)

    except KeyboardInterrupt:
        print("Program exited")
        led_controller.clean_up()