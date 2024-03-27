#!/usr/bin/env python

import grove.i2c
from sensors import AReading, ISensor

from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep

class Sensor(ISensor): 
    def __init__(self, gpio: int, model: str, type: AReading.Type):
        #self.sensor = GroveTemperatureHumidityAHT20(0x38, 4)
        print("Yeah I did stuff")

    def read_sensor(self) -> list[AReading]:
        #return self.sensor.read()
        print("NOT IMPLEMENTED YET")

sensor = Sensor(1, "H", AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, 1))
temp = sensor.read_sensor()


