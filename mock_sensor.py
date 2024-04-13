from sensors import AReading, ISensor
from time import sleep


class MockSensor(ISensor):
    _sensor_model: str
    reading_type: AReading.Type

    # gpio replaces bus num
    def __init__(self, gpio: int,  model: str, type: AReading.Type):
        self._sensor_model = model
        self.reading_type = type

    def read_sensor(self) -> list[AReading]:
        print(f"{self.reading_type.name} On")
        unit = AReading.Unit.UNITLESS
        if self.reading_type == AReading.Type.TEMPERATURE:
            unit = AReading.Unit.CELCIUS
        elif self.reading_type == AReading.Type.HUMIDITY:
            unit = AReading.Unit.HUMIDITY
        elif self.reading_type == AReading.Type.LUMINOSITY:
            unit = AReading.Unit.LUX

        return [
            AReading(self.reading_type, unit, 0)
        ]


def main():
    tempsensor = MockSensor(4, "AHT20", AReading.Type.TEMPERATURE)
    humisensor = MockSensor(4, "AHT20", AReading.Type.HUMIDITY)
    lumisensor = MockSensor(4, "reterminal", AReading.Type.LUMINOSITY)
    while True:
        print("Random sensor readings in 2 seconds...")
        sleep(1)
        print(tempsensor.read_sensor())
        print(humisensor.read_sensor())
        print(lumisensor.read_sensor())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
