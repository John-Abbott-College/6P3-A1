from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep
from sensors import AReading, ISensor


class TempHumiditySensor(ISensor):
    _sensor_model: str
    reading_type: AReading.Type

    #gpio replaces bus num
    def __init__(self, gpio: int,  model: str, type: AReading.Type):
        address:hex=0x38
        self.sensor = GroveTemperatureHumidityAHT20(address = address, bus=4)
        self._sensor_model = model
        self.reading_type = type

    def read_sensor(self) -> list[AReading]:
        temperature, humidity = self.sensor.read()
        return list([
            AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, temperature),
            AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, humidity)
        ]
        )
    

def main():
    sensor = TempHumiditySensor()
    while True:
        temperature, humidity = sensor.read_sensor()
        print('Temperature in Celsius is {:.2f} C'.format(temperature.value))
        print('Relative Humidity is {:.2f} %'.format(humidity.value))
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
