#!/usr/bin/env python3

from grove.i2c import Bus
from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
import time
from typing import List, NamedTuple, Literal, Union, Any
from datetime import datetime
from sensors import ISensor, AReading

AHT20_ADDRESS = 0x38
BUS = 4

class Reading(NamedTuple):
    """A class to represent a sensor reading with additional information."""
    value: float
    unit: str
    timestamp: str

    def __str__(self):
        formatted_value = "{:.2f}".format(self.value)
        return f"{formatted_value} {self.unit} at {self.timestamp}"


class TemperatureHumiditySensor():
    """A class to represent a sensor with a method to read tempature and humidity."""

    def __init__(self, address: int, bus: Union[Any, int]) -> None:
        """
        Initialize the Temperature and humidiy sensor and sets the address and bus.

            Args:
            - address: The address of the sensor.
            - bus: The i2c bus the sensor is connected to.
        """
        self.sensor = GroveTemperatureHumidityAHT20(address=address, bus=bus)

    def read_sensor(self) -> List[Reading]:
        """
        Reads sensor data and returns a list of readings.
        
        Returns:
        List[Reading]: A list of the readings taken by the sensor.
        """
        temperature, humidity = self.sensor.read()    
        temp_reading = Reading(value=temperature, unit="C", timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        humidity_reading = Reading(value=humidity, unit="% Humidity", timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

        return [temp_reading, humidity_reading]


def main():
    sensor = TemperatureHumiditySensor(address = AHT20_ADDRESS, bus = BUS)
    while True:
        readings = sensor.read_sensor()
        for reading in readings:
            print(reading)

        time.sleep(1)


if __name__ == "__main__":
    main()
