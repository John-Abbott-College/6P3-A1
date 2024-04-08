from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from sensors import AReading, ISensor
from dotenv import load_dotenv
from time import sleep
import os


class TempHumiditySensor(ISensor):
    _sensor_model: str
    reading_type: AReading.Type

    #gpio replaces bus num
    def __init__(self, gpio: int,  model: str, type: AReading.Type):
        address:hex=0x38
        if os.environ['PROD_MODE_ON']:
            self.sensor = GroveTemperatureHumidityAHT20(address = address, bus=4)
        self._sensor_model = model
        self.reading_type = type

    def read_sensor(self) -> list[AReading]:
        if os.environ['PROD_MODE_ON']:
            temperature, humidity = self.sensor.read()
            return list([
                AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, temperature),
                AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, humidity)
            ])
        else:
            print('ON')
            return None
    

def main():
    load_dotenv()
    sensor = TempHumiditySensor()
    while True:
        if sensor.read_sensor() != None:
            temperature, humidity = sensor.read_sensor()
            print('Temperature in Celsius is {:.2f} C'.format(temperature.value))
            print('Relative Humidity is {:.2f} %'.format(humidity.value))
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
