from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep
from sensors import AReading, ISensor


class TempHumiditySensor(ISensor): 
    def __init__(self, address:hex=0x38, bus:int=4) -> None:
        self.sensor = GroveTemperatureHumidityAHT20(address = address, bus = bus)

    def read_sensor(self) -> list[AReading]: 
        temperature, humidity = self.sensor.read()

        return [AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, temperature), AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, humidity)]
    

def main():
    sensor = TempHumiditySensor()
    while True:
        readings = sensor.read_sensor()
        temperature_reading = readings[0]
        humidity_reading = readings[1]

        print('Temperature in Celsius is {:.2f} C'.format(temperature_reading.value))
        print('Relative Humidity is {:.2f} %'.format(humidity_reading.value))
        sleep(1)



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass