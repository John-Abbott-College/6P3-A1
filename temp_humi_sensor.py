from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from sensors import ISensor, AReading

class TempHumiController(ISensor):

    def __init__(self, gpio: int, model: str, type: AReading.Type):
        self.gpio = gpio
        self.model = model
        self.type = type
        self.temperature = GroveTemperatureHumidityAHT20(bus=gpio)

    def read_sensor(self):
        temperature, humidity = self.temperature.read()

        return [
            AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, temperature),
            AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, humidity)
        ]
    
    
if __name__ == "__main__":
    temp = TempHumiController(4, "AHT20", AReading.Type.TEMPERATURE)
    while True:
        temperature, humidity = temp.read_sensor()