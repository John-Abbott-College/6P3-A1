from temperature_sensor import TemperatureSensor
from humidity_sensor import HumiditySensor
from sensors import AReading
import random

class MockTemperatureSensor(TemperatureSensor):
    def __init__(self, gpio: int,  model: str, type: AReading.Type):
        self._sensor = "TemperatureSensor"
        self._sensor_model = model
        self.reading_type = type

    def read_sensor(self) -> list[AReading]:
        random_temperature = 20 + int(random.random() * 5)
        return [ 
            AReading(self.reading_type, AReading.Unit.CELCIUS, random_temperature) 
        ]

class MockHumiditySensor(HumiditySensor):
    def __init__(self, gpio: int,  model: str, type: AReading.Type):
        self._sensor = "HumiditySensor"
        self._sensor_model = model
        self.reading_type = type

    def read_sensor(self) -> list[AReading]:
        random_humidity = 60 + int(random.random() * 10)
        return [ 
            AReading(self.reading_type, AReading.Unit.HUMIDITY, random_humidity) 
        ]
