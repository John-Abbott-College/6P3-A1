#!/usr/bin/env python3

from gpiozero import PWMLED
from time import sleep
from actuators import IActuator, ACommand

LED_GPIO_PIN = 12

class LEDController(IActuator):

    def __init__(self, gpio: int, type: ACommand.Type, initial_state: str = "off") -> None:
        """
        Initialize the LED controller.

        Args:
        - gpio: The GPIO pin connected to the LED.
        - type: The type of command this actuator responds to (should be LIGHT_ON_OFF or LIGHT_PULSE).
        - initial_state: The initial state of the LED ("on", "off", or a pulse duration as a string).
        """
        self._current_state = initial_state
        self.type = type
        self.led = PWMLED(gpio)

    def validate_command(self, command: ACommand) -> bool:
        """Validates that a command can be used with the LED actuator.

        Args:
            command (ACommand): The command to be validated.

        Returns:
            bool: True if the command is compatible, false otherwise.
        """
        if command.target_type == self.type:
            if type(command.value) is str and (command.value.lower() =="on" or command.value.lower() == "off") and self.type == ACommand.Type.LIGHT_ON_OFF:
                return True
            elif type(command.value) is str and command.value.isnumeric() and self.type == ACommand.Type.LIGHT_PULSE:
                return True
            else:
                return False
            
        return False
    
    def control_actuator(self, value: str) -> bool:
        """
        Sets the LED based on the value. The value can be "on", "off", or a pulse duration.

        Args:
            value (str): The command value as a string.  

        Returns:
            bool: True if the command was executed successfully, False otherwise.
        """
        if value.lower() == "on":
            self.led.on()
            self._current_state = "on"
            return True
        elif value.lower() == "off":
            self.led.off()
            self._current_state = "off"
            return True
        else:
            try:
                pulse_duration = float(value)
                if pulse_duration <= 0:
                    return False
                
                self.led.pulse(fade_in_time=pulse_duration/2, 
                               fade_out_time=pulse_duration/2,
                               n=1,
                               background=True)
                self._current_state = value
                return True
            except ValueError:
                return False
            
    def clean_up(self):
        """Cleans up the device"""
        self.led.off()

if __name__ == "__main__":
    led_controller = LEDController(LED_GPIO_PIN, ACommand.Type.LIGHT_PULSE, "off") 
    try:
        while True:
            led_controller.control_actuator("2")
            sleep(4)

    except KeyboardInterrupt:
        print("Program exited")
        led_controller.clean_up()