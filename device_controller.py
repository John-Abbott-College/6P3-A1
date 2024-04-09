from sensors import ISensor, AReading
from actuators import IActuator, ACommand
from temp_humi_sensor import TempController
from fan_control import FanController
from led_pwm import LEDController
from time import sleep

class DeviceController:

    def __init__(self):
        self._sensors = self._init_sensors()
        self._actuators = self._init_actuators()

    def _init_sensors(self) -> list[ISensor]:
        return [TempController(bus=4, model="AHT20", reading_type=AReading.Type.TEMPERATURE)]

    def _init_actuators(self) -> list[IActuator]:
        return [
            LEDController(pin=16, cmd_type=ACommand.Type.LIGHT_PULSE, state="OFF"),
            FanController(pin=22, cmd_type=ACommand.Type.FAN, state="OFF"),
        ]

    def read_sensors(self) -> list[AReading]:
        data = []
        for device in self._sensors:
            data += device.read_sensor()
        return data

    def control_actuators(self, cmds: list[ACommand]) -> None:
        for cmd in cmds:
            for device in self._actuators:
                if device.validate_command(cmd):
                    device.control_actuator(cmd.value)

if __name__ == "__main__":
    hub = DeviceController()
    test_interval = 3

    while True:
        sensor_readings = hub.read_sensors()
        print(sensor_readings)

        on_cmds = [
            ACommand(target=ACommand.Type.FAN, value="ON"),
            ACommand(target=ACommand.Type.LIGHT_PULSE, value="ON"),
        ]
        hub.control_actuators(on_cmds)
        sleep(test_interval)

        off_cmds = [
            ACommand(target=ACommand.Type.FAN, value="OFF"),
            ACommand(target=ACommand.Type.LIGHT_PULSE, value="OFF"),
        ]
        hub.control_actuators(off_cmds)
        sleep(test_interval)
