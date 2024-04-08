from device_controller import DeviceController
from connection_manager import ConnectionManager


class Hvac:

    DEBUG = True

    def __init__(self) -> None:
        self._device_manager = DeviceController()
        self._connection_manager = ConnectionManager()

    def loop(self) -> None:
        """Main loop of the HVAC System. Collect new readings, send them to connection
        manager, collect new commands and dispatch them to device manager.
        """

        self._connection_manager.connect()

        while True:
            # Collect new readings
            readings = self._device_manager.read_sensors()
            if self.DEBUG:
                print(readings)

            # Send collected readings
            self._connection_manager.send_readings(readings)

            # Receive commands from the cloud
            commands = self._connection_manager.receive_commands()
            if self.DEBUG:
                print(commands)

            # Dispatch commands to device manager
            self._device_manager.control_actuators(commands)


# Will only run if file is executed as a script by python interpreter
if __name__ == "__main__":
    hvac = Hvac()
    hvac.loop()