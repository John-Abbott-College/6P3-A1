import sys
sys.path.append("/home/zakarigaudreault/lab4")

from abc import ABC, abstractmethod
from enum import Enum
from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
import time
from typing import Union

class AReading(ABC):
    """Abstract class for sensor readings. Can be instantiated directly or inherited.
    Also defines all possible types of readings and reading units using enums.
    """

    class Type(str, Enum):
        """Enum defining all possible types of readings that sensors might make.
        """
        # Add new reading types here.
        TEMPERATURE = 'temperature'
        HUMIDITY = 'humidity'
        LUMINOSITY = 'luminosity'

    class Unit(str, Enum):
        """Enum defining all possible units for sensor measuremens.
        """
        # Add new reading units here.
        MILLIMITERS = 'mm'
        CELCIUS = '°C'
        FAHRENHEIT = '°F'
        HUMIDITY = '% HR'
        UNITLESS = 'unitless'

    # Class properties that must be defined in implementation classes
    reading_type: Type
    reading_unit: Unit
    value: float

    def __init__(self, type: Type, unit: Unit, value: float) -> None:
        self.reading_type = type
        self.reading_unit = unit
        self.value = value

    def __repr__(self) -> str:
        """String representation of a reading object
        """
        return f"{self.reading_type}: {self.value} {self.reading_unit}"


class ISensor(ABC):
    """Interface for all sensors.
    """

    # Class properties that must be defined in implementation classes
    _sensor_model: str
    reading_type: AReading.Type

    @abstractmethod
    def __init__(self, gpio: int,  model: str, type: AReading.Type):
        """Constructor for Sensor  class. May be called from childclass.

        :param str model: specific model of sensor hardware. Ex. AHT20 or LTR-303ALS-01
        :param ReadingType type: Type of reading this sensor produces. Ex. 'TEMPERATURE'
        """

    @abstractmethod
    def read_sensor(self, unit: AReading.Unit) -> list[AReading]:
        """Takes a reading form the sensor

        :param Unit unit: Desired unit for temperature readings
        :return list[AReading]: List of readings measured by the sensor. Most sensors return a list with a single item.
        """
        pass


class HumiditySensor(ISensor):
    def __init__(self, gpio: int, model: str, type: AReading.Type, address: hex = 0x38, bus: int = 4) -> None:
        self.gpio = gpio
        self.model = model
        self.type = type
        self.address = address
        self.bus = bus
        self.sensor = None
        try:
            self.sensor = GroveTemperatureHumidityAHT20(address=address, bus=bus)
        except OSError as e:
            print("Error initializing sensor:", e)
    
    def read_sensor(self, unit: AReading.Unit) -> Union[tuple, None]:
        if self.sensor:
            try:
                temperature_c, humidity = self.sensor.read()
                temperature = temperature_c if unit == AReading.Unit.CELCIUS else self._celsius_to_fahrenheit(temperature_c)
                return (temperature, humidity)
            except OSError as e:
                print("Error reading sensor:", e)
                return None
        else:
            print("Sensor not initialized.")
            return None

    def _celsius_to_fahrenheit(self, temperature_c: float) -> float:
        """Convert Celsius temperature to Fahrenheit."""
        return (temperature_c * 9/5) + 32

if __name__ == "__main__":
    sensor = HumiditySensor(gpio=0, model="dummy_model", type=AReading.Type.HUMIDITY)
    
    while True:
        sensor_reading = sensor.read_sensor()
        if sensor_reading:
            print(sensor_reading)
        time.sleep(2)
