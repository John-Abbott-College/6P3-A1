from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from sensors import ISensor, AReading
from time import sleep


class TempHumiditySensor(ISensor): 
    def __init__(self, gpio: int,  model: str, type: AReading.Type):
        """Constructor for Sensor  class. May be called from childclass.

        :param int gpio: bus number for the sensor
        :param str model: specific model of sensor hardware. Ex. AHT20 or LTR-303ALS-01
        :param ReadingType type: Type of reading this sensor produces. Ex. 'TEMPERATURE'
        """
        self._sensor_model = model
        self.reading_type = type
        self.sensor = GroveTemperatureHumidityAHT20(bus = gpio)

    def read_sensor(self) -> list[AReading]:
        """Reads the sensor to get the temperature and humidity.
        """
        temperature, humidity = self.sensor.read() 
        return [
            AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, temperature),
            AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, humidity)
        ]
    

def main():
    sensor = TempHumiditySensor(4, "AHT20", AReading.Type.TEMPERATURE)
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
