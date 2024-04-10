from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep
from abc import ABC, abstractmethod
from sensors import ISensor, AReading


class TempHumiditySensor(ISensor):
    def __init__(self, gpio: int, model: str, type: AReading.Type, address: hex = 0x38, bus: int = 4):
        self.gpio = gpio
        self.model = model
        self.type = type
        self.sensor = GroveTemperatureHumidityAHT20(address=address, bus=bus)

    def read_sensor(self):
        temperature, humidity = self.sensor.read()
        readings = [
            AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, temperature),
            AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, humidity)
        ]
        return readings
