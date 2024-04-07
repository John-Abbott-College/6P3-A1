from gpiozero import OutputDevice
from time import sleep
from typing import Union

class FanController:
    def __init__(self, relay_pin: int):
        self.relay = OutputDevice(relay_pin)

    def control_actuator(self, new_state: str) -> bool:
        if new_state.lower() == "on":
            self.relay.on()
            return True
        elif new_state.lower() == "off":
            self.relay.off()
            return True
        else:
            return False
##
if __name__ == "__main__":
    relay_pin = 16  
    fan_controller = FanController(relay_pin)

    try:
        while True:
            fan_controller.control_actuator("on")
            sleep(2)
            fan_controller.control_actuator("off")
            sleep(2)
    except KeyboardInterrupt:
        print("Fan control interrupted.")
