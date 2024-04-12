from connection_manager import ConnectionManager
from device_controller import DeviceController

from time import sleep

class Hvac:
    DEBUG = True
    def __init__(self) -> None:
        self._connection_manager = ConnectionManager()
        self._device_manager = DeviceController()

    def loop(self) -> None:
        self._connection_manager.connect()

        while True:
            # Collect new readings
            readings = self._device_manager.read_sensors()
            if self.DEBUG:
                print("sensor read:", readings)

            # Send collected readings
            self._connection_manager.send_readings(readings)

            # Receive commands from the cloud
            commands = self._connection_manager.receive_commands()
            if self.DEBUG:
                print("recieved commands:", commands)

            # Dispatch commands to device manager
            self._device_manager.control_actuators(commands)

            sleep(1)


# Will only run if file is executed as a script by python interpreter
if __name__ == "__main__":
    hvac = Hvac()
    hvac.loop()