from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep
from sensors import ISensor,AReading


class TempHumiditySensor(ISensor): 
    def __init__(self, gpio: int,  model: str, type: AReading.Type):
        self.sensor = GroveTemperatureHumidityAHT20(bus = gpio)
        self.model = model
        self.type = type

    def read_sensor(self) -> list[AReading]:
        temperature, humidity = self.sensor.read()

        return[
           AReading(AReading.Type.TEMPERATURE,AReading.Unit.CELCIUS,temperature),
           AReading(AReading.Type.HUMIDITY,AReading.Unit.HUMIDITY,humidity)
        ]
    

def main():
    sensor = TempHumiditySensor()
    while True:
        temperature, humidity = sensor.read_sensor()
        print('Temperature in Celsius is {:.2f} C'.format(temperature))
        print('Relative Humidity is {:.2f} %'.format(humidity))
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
