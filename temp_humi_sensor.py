#!/usr/bin/env python
from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep
from sensors import ISensor,AReading

class TempHumiditySensor(ISensor): 
    #add sub item for humitdy and one for temp so read sensor returns the correct item based on input
    def __init__(self, address:hex=0x38, bus:int=4,type = AReading) -> None:
        super(ISensor, self).__init__()
        self.sensor = GroveTemperatureHumidityAHT20(address = address, bus = bus)
        self.type = type
        
        

    def _read_sensor(self) -> list[float]: 
        return list(self.sensor.read())
    

    def read_sensor(self) -> list[AReading]:
        """Takes a reading form the sensor

        :return list[AReading]: List of readinds measured by the sensor. Most sensors return a list with a single item.
        """
        if self.type == AReading.Type.TEMPERATURE:
            temp, humidity = self._read_sensor()
            return[
            AReading(value=temp,type=AReading.Type.TEMPERATURE,unit=AReading.Unit.CELCIUS)
            ]
        else:
            temp, humi = self._read_sensor()
            return[
                 AReading(value=humi,type=AReading.Type.HUMIDITY,unit=AReading.Unit.HUMIDITY)
            ]
    

def main():
    sensor = TempHumiditySensor(type = AReading.Type.TEMPERATURE)
    while True:
        temperature, humidity = sensor._read_sensor()
        #instead of the above temp, _ = self.read_sensor() will only keep temp and trash humi, opposite works as well.
        print('Temperature in Celsius is {:.2f} C'.format(temperature))
        print('Relative Humidity is {:.2f} %'.format(humidity))
        sleep(1)


    


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
