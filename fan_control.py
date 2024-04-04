from gpiozero import LED
from time import sleep

class FanController:
    def __init__(self, pin: int) -> None:
        self.fan = LED(pin)
        self._state = False

    def control_actuator(self, state: bool) -> bool:
        if state:
            self.fan.on()
        else:
            self.fan.off()

        ret = self._state != state
        self._state = state
        return ret

    def get_state(self) -> bool:
        return self._state

if __name__ == "__main__":
    fan = FanController(22)
    while True:
        print(fan.control_actuator(True))
        sleep(2)
        print(fan.control_actuator(False))
        sleep(2)