#!/usr/bin/env python3

from grove.i2c import Bus
from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
import time
from typing import List, NamedTuple, Literal, Union, Any
from datetime import datetime
from sensors import ISensor, AReading

AHT20_ADDRESS = 0x38
BUS = 4

class SensorReading(AReading):
    """A class to represent a sensor reading with additional information."""

    def __init__(self, type: 'AReading.Type', unit: 'AReading.Unit', value: float):
        super().__init__(type, unit, value)

    def __repr__(self) -> str:
        return f"{self.reading_type.value.capitalize()}: {self.value:.2f}{self.reading_unit.value}"


class TemperatureHumiditySensor(ISensor):
    """A class to represent a sensor with a method to read tempature and humidity."""

    def __init__(self, gpio: int, model: str, type: AReading.Type ) -> None:
        """
        Initialize the Temperature and humidiy sensor and sets the model and reading type.

            Args:
            - gpio (int): The address of the sensor.
            - model (str): specific model of sensor hardware. Should be AHT20.
            - type (AReading.Type): Type of reading produced by sensor. Should be 'TEMPERATURE' or 'HUMIDITY'
        """
        self.sensor = GroveTemperatureHumidityAHT20(address=AHT20_ADDRESS, bus=gpio)
        self._sensor_model = model
        self.reading_type = type

    def read_sensor(self) -> List[AReading]:
        """
        Reads sensor data and returns a list of readings.
        
        Returns:
        List[AReading]: A list of the readings taken by the sensor.
        """
        temperature, humidity = self.sensor.read()
        readings = []

        if AReading.Type.TEMPERATURE in self.reading_type:
            readings.append(SensorReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, temperature))
        if AReading.Type.HUMIDITY in self.reading_type:
            readings.append(SensorReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, humidity))

        return readings


def main():
    # type shouldn't be a list but it works :)
    sensor = TemperatureHumiditySensor(gpio=BUS, model="AHT20", type=[AReading.Type.TEMPERATURE, AReading.Type.HUMIDITY])
    while True:
        readings = sensor.read_sensor()
        for reading in readings:
            print(reading)

        time.sleep(1)


if __name__ == "__main__":
    main()
