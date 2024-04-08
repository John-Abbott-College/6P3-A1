#!/usr/bin/env python
from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep
from sensors import ISensor,AReading


class TempHumiditySensor(ISensor): 
    def __init__(self, address:hex=0x38, bus:int=4) -> None:
        self.sensor = GroveTemperatureHumidityAHT20(address = address, bus = bus)
        self._sensor_model = 'GroveTemperatureHumidityAHT20'

    def read_sensor(self) -> list[AReading]: 
        temp, humidity = self.sensor.read()
        return [
            AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, temp),
            AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, humidity)
        ]
    

def main():
    sensor = TempHumiditySensor()
    while True:
        readings = sensor.read_sensor()
        print(f"Temperature in Celsius is {readings[0].value} C")
        print(f"Relative Humidity is {readings[1].value}%")
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
