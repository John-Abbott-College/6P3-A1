from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
import seeed_python_reterminal.core as rt
from time import sleep
from sensors import ISensor, AReading


class TemperatureHumiditySensor(ISensor):
    """
    A sensor class for reading Temperature and/or Humidity

    Implements the ISensor interface

    Attributes:
        gpio (int): I'm actually using this as the bus number...
        model (str): The model of the temperature controller.
        type (AReading.Type): The type of the sensor reading.

    Methods:
        read_sensor(): Reads the temperature and humidity from the sensor.

    """

    def __init__(self, gpio: int, model: str, type: AReading.Type):
        """
        Initialize a TempHumiSensor object.

        Args:
            gpio (int): The GPIO pin number.
            model (str): The model of the temperature and humidity sensor.
            type (AReading.Type): The type of reading (e.g., temperature or humidity).

        Returns:
            None

        """
        self.sensor = GroveTemperatureHumidityAHT20(address=0x38, bus=gpio)
        self.model = model
        self.type = type

    def read_sensor(self) -> list[AReading]:
        """
        Takes a reading from the temperature and humidity sensor.

        Args: none

        Returns:
            list[AReading]: a list of temperature and humidity readings.

        """
        if self.type == AReading.Type.TEMPERATURE:
            return self._read_temp()
        elif self.type == AReading.Type.HUMIDITY:
            return self._read_humi()
        else:
            return []

    def _read_temp(self) -> AReading:
        temperature, _ = self.sensor.read()
        return AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS.value, temperature),

    def _read_humi(self) -> AReading:
        _, humidity = self.sensor.read()
        return AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY.value, humidity),



class ReTerminalSensor(ISensor):
    """
    A sensor class for reading Temperature and/or Humidity

    Implements the ISensor interface

    Attributes:
        gpio (int): I'm actually using this as the bus number...
        model (str): The model of the temperature controller.
        type (AReading.Type): The type of the sensor reading.

    Methods:
        read_sensor(): Reads the temperature and humidity from the sensor.

    """

    def __init__(self, gpio: int, model: str, type: AReading.Type):
        """
        Initialize a reTerminal sensor object.

        Args:
            gpio (int): The GPIO pin number.
            model (str): The model of the temperature and humidity sensor.
            type (AReading.Type): The type of reading (e.g., temperature or humidity).

        Returns:
            None

        """
        self.gpio = gpio
        self.model = model
        self.type = type


    def read_sensor(self) -> list[AReading]:
        """
        Takes a reading from the temperature and humidity sensor.

        Args: none

        Returns:
            list[AReading]: a list of temperature and humidity readings.

        """
        luminosity = rt.illuminance
        return [
            AReading(AReading.Type.LUMINOSITY, AReading.Unit.LUX, luminosity),
        ]


def main():
    tempsensor = TemperatureHumiditySensor(4, "AHT20", AReading.Type.TEMPERATURE.value)
    humisensor = TemperatureHumiditySensor(4, "AHT20", AReading.Type.HUMIDITY.value)
    lumisensor = ReTerminalSensor(4, "reTerminal", AReading.Type.LUMINOSITY.value)
    while True:
        print(tempsensor.read_sensor())
        print(humisensor.read_sensor())
        print(lumisensor.read_sensor())
        sleep(2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass