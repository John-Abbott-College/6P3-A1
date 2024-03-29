#!/usr/bin/env python

import grove.i2c
from sensors import AReading, ISensor

from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep

class Sensor(ISensor): 
    _sensor_model: str
    reading_type: AReading.Type

    def __init__(self, gpio: int, model: str, type: AReading.Type):
        self._sensor_model = model
        self.reading_type = type

        self.sensor = GroveTemperatureHumidityAHT20(0x38, 4)

    def read_sensor(self) -> list[AReading]:
        _temperature, _humidity = 0, 1
        _reading = self.sensor.read()

        return [AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, _reading[_temperature]),
            AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, _reading[_humidity])]

# sensor = Sensor(1, "AH20", AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, 1))
# temp = sensor.read_sensor()
# print(temp)


