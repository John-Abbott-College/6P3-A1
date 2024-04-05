from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from sensors import ISensor, AReading

class TemperatureSensor(ISensor):
    def __init__(self, gpio: int,  model: str, type: AReading.Type):
        self._sensor = GroveTemperatureHumidityAHT20(0x38, gpio)
        self._sensor_model = model
        self.reading_type = type

    def read_sensor(self) -> list[AReading]:
        temperature, _ = self._sensor.read()
        return [ 
            AReading(self.reading_type, AReading.Unit.CELCIUS, temperature) 
        ]

if __name__ == "__main__":
    import time
    sensor = TemperatureSensor(4, "AHT20", AReading.Type.TEMPERATURE)
    while True:
        print(sensor.read_sensor())
        time.sleep(0.5)
