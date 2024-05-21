from sensors import AReading
from time import sleep
from temp_humi_sensor import TempHumiditySensor
from random import randrange


class MockTempHumiditySensor(TempHumiditySensor):
    def __init__(self, gpio: int,  model: str, type: AReading.Type):
        """Constructor for Sensor  class. May be called from childclass.

        :param int gpio: bus number for the sensor
        :param str model: specific model of sensor hardware. Ex. AHT20 or LTR-303ALS-01
        :param ReadingType type: Type of reading this sensor produces. Ex. 'TEMPERATURE'
        """
        self._sensor_model = model
        self.reading_type = type

    def read_sensor(self) -> list[AReading]:
        """Reads the sensor to get the temperature and humidity.
        """
        return [
            AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, randrange(-50, 100)),
            AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, randrange(-50, 100))
        ]
    

def main():
    sensor = MockTempHumiditySensor(4, "AHT20", AReading.Type.TEMPERATURE)
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