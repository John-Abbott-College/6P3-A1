from random import random
from time import sleep
from . import ISensor, AReading


class MockSensor(ISensor):
    """
    A mock temperature/humidiry sesnro

    Attributes:
        temp (str): The temperature sensor bus number.
        model (str): The model of the temperature and humidity sensor.
        type (AReading.Type): The type of reading (e.g., temperature or humidity).

    """

    def __init__(self, gpio: int, model: str, type: AReading.Type):
        """
        Initialize a TempController object.

        Args:
            gpio (int): The GPIO pin number.
            model (str): The model of the temperature and humidity sensor.
            type (AReading.Type): The type of reading (e.g., temperature or humidity).

        Returns:
            None

        """
        self.sensor = f"{model}_bus_{gpio}"
        self.model = model
        self.type = type

    def read_sensor(self) -> list[AReading]:
        """
        Reads the temperature and humidity from the sensor.

        Returns:
            list[AReading]: A list of AReading objects representing the temperature and humidity readings.

        """
        unit = AReading.Unit.UNITLESS
        if self.type == AReading.Type.TEMPERATURE:
            unit = AReading.Unit.CELSIUS
        elif self.type == AReading.Type.HUMIDITY:
            unit = AReading.Unit.HUMIDITY
        elif self.type == AReading.Type.LUMINOSITY:
            unit = AReading.Unit.LUX

        return [
            AReading(self.type, unit, random() * 100),
        ]


def main():
    tempsensor = MockSensor(4, "AHT20", AReading.Type.TEMPERATURE)
    humisensor = MockSensor(4, "AHT20", AReading.Type.HUMIDITY)
    lumisensor = MockSensor(4, "reterminal", AReading.Type.LUMINOSITY)
    while True:
        print("Random sensor readings in 2 seconds...")
        sleep(2)
        print(tempsensor.read_sensor())
        print(humisensor.read_sensor())
        print(lumisensor.read_sensor())


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass