from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep

from sensors import ISensor, AReading

class TempHumiditySensor(ISensor): 
    def __init__(self,gpio: int,  model: str, type: AReading.Type, address:hex=0x38, bus:int=4) -> None:
        self.gpio = gpio
        self.model = model
        self.type = type
        self.sensor = GroveTemperatureHumidityAHT20(address = address, bus = bus)

    def read_sensor(self) -> list[float]: 
        return list(self.sensor.read())
    

def main():
    sensor = TempHumiditySensor(gpio=26, model="AHT20", type=AReading.Type.TEMPERATURE)
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
