from fan_control import FanActuator
from led_pwm import LEDActuator
from temp_humi_sensor import TempHumiditySensor
from time import sleep


class Device_Controller:
    def __init__(self) -> None:
        self.led = LEDActuator(gpio=12)
        self.fan = FanActuator(gpio=16)
        self.sensor = TempHumiditySensor()

    def control_actuators(self) -> None:
        led_duration = "1" if self.led.duration == "2" else "2"
        self.led.control_actuator(led_duration)
        fan_state = "1" if self.fan.current_state == "0" else "0"
        self.fan.control_actuator(fan_state)

    def read_sensors(self) -> None:
        print(f"{self.sensor.read_sensor()}") 

    def loop(self):
        while True:
            self.control_actuators()
            self.read_sensors()
            sleep(2)


def main():
    controller = Device_Controller()
    controller.loop()


if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        pass
