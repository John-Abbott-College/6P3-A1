from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
from sensors import ISensor, AReading
from time import sleep

class TempHumiditySensor(ISensor):
    def __init__(self, address: hex = 0x38, bus: int = 4) -> None:
        self._sensor_model = "AHT20"
        self._address = address
        self._bus = bus
        self.sensor = GroveTemperatureHumidityAHT20(address=address, bus=bus)
        self.reading_type = AReading.Type.TEMPERATURE  # Assuming this sensor is primarily a temperature sensor

    def read_sensor(self) -> list[AReading]:
        temperature, humidity = self.sensor.read()
        return [
            AReading(type=AReading.Type.TEMPERATURE, unit=AReading.Unit.CELCIUS, value=temperature),
            AReading(type=AReading.Type.HUMIDITY, unit=AReading.Unit.HUMIDITY, value=humidity)
        ]

def main():
    sensor = TempHumiditySensor()
    while True:
        readings = sensor.read_sensor()
        for reading in readings:
            print(f'{reading.reading_type.value}: {reading.value} {reading.reading_unit.value}')
        sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
