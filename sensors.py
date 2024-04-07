import sys
sys.path.append("/home/zakarigaudreault/lab4") 

from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
import time
from typing import Union

class HumiditySensor:
    def __init__(self, address: hex = 0x38, bus: int = 4) -> None:
        self.address = address
        self.bus = bus
        self.sensor = None
        try:
            self.sensor = GroveTemperatureHumidityAHT20(address=address, bus=bus)
        except OSError as e:
            print("Error initializing sensor:", e)
    
    def read_sensor(self) -> Union[tuple, None]:
        if self.sensor:
            try:
                return self.sensor.read()
            except OSError as e:
                print("Error reading sensor:", e)
                return None
        else:
            print("Sensor not initialized.")
            return None

if __name__ == "__main__":
    sensor = HumiditySensor()
    
    while True:
        sensor_reading = sensor.read_sensor()
        if sensor_reading:
            print(sensor_reading)
        time.sleep(2)
