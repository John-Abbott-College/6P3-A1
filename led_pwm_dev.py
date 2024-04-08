#!/usr/bin/env python
from gpiozero import PWMLED
from signal import pause

from actuators import IActuator,ACommand

class LEDActuatorDev(IActuator):
    def __init__(self,type: ACommand) -> None:
        super(IActuator, self).__init__()
        self.duration = 0
        self.type = type

    def validate_command(self,command:ACommand) -> bool:
       return command.value < 0
    
    def control_actuator(self, value:str) -> bool:
        previous_duration = self.duration
        self.duration = float(value)
        return previous_duration != self.duration


def main():
    led = LEDActuatorDev(gpio=12,type=ACommand.Type.LIGHT_PULSE)
    duration = 2
    print(f"LED pulsing twice for {duration} seconds...")
    led.control_actuator(duration)
    print(f"Finished. Press CTRL-C to exit.")
    pause()


if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        pass
