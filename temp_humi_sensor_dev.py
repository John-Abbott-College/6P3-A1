#!/usr/bin/env python
from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep
from sensors import ISensor,AReading
import random

class TempHumiditySensorDev(ISensor): 
    #add sub item for humitdy and one for temp so read sensor returns the correct item based on input
    def __init__(self,type = AReading) -> None:
        super(ISensor, self).__init__()
        self.type = type
        
        

    def _read_sensor(self) -> list[float]: 
        return list(self.sensor.read())
    

    def read_sensor(self) -> list[AReading]:
        """Takes a reading form the sensor

        :return list[AReading]: List of readinds measured by the sensor. Most sensors return a list with a single item.
        """
        if self.type == AReading.Type.TEMPERATURE:
            
            return[
            AReading(value=round(random.uniform(20,40), 2),type=AReading.Type.TEMPERATURE,unit=AReading.Unit.CELCIUS)
            ]
        else:
            
            return[
                 AReading(value=round(random.uniform(10,90), 2),type=AReading.Type.HUMIDITY,unit=AReading.Unit.HUMIDITY)
            ]
    

def main():
    sensor = TempHumiditySensorDev(type = AReading.Type.TEMPERATURE)
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
