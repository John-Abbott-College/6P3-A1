from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from time import sleep


class TempHumiditySensor:
    def __init__(self, address: hex = 0x38, bus: int = 4) -> None:
        self.sensor = GroveTemperatureHumidityAHT20(address=address, bus=bus)

    def read_sensor(self) -> list[float]:
        return list(self.sensor.read())


def main():
    sensor = TempHumiditySensor()
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
