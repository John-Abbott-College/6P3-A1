from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep
from sensors import ISensor, AReading


class TempHumiditySensor(ISensor): 
    def __init__(self, gpio: int,  model: str, command_type: AReading.Type, address:hex=0x38, bus:int=4) -> None:
        self.sensor = GroveTemperatureHumidityAHT20(address = address, bus = bus)
        self.gpio = gpio
        self.model = model
        self.type = command_type

    def read_sensor(self) -> list[AReading]: 
        return list(self.sensor.read())
    

def main():
    sensor = TempHumiditySensor(gpio=26, model="AHT20", command_type=AReading.Type.TEMPERATURE)
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
