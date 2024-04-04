from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from sensors import ISensor, AReading

class HumiditiySensor(ISensor):
    @ISensor.__init__
    def __init__(self, gpio: int,  model: str, type: AReading.Type):
        self._sensor = GroveTemperatureHumidityAHT20(0x38, gpio)
        self._sensor_model = model
        self.reading_type = type

    @ISensor.read_sensor
    def read_sensor(self) -> list[AReading]:
        _, humidity = self._sensor.read()
        return [ AReading(self.reading_type, AReading.Unit.HUMIDITY, humidity) ]
