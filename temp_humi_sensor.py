from grove.grove_temperature_humidity_aht20 import GroveTemperatureHumidityAHT20
import time

class TempHumiReading:
    def __init__(self, temperature: float, humidity: float) -> None:
        self.temperature = temperature
        self.humidity = humidity

class TempHumiSensor:
    def __init__(self, bus) -> None:
        self._sensor = GroveTemperatureHumidityAHT20(0x38, bus)

    def read_sensor(self) -> TempHumiReading:
        temperature, humidity = self._sensor.read()
        return TempHumiReading(temperature, humidity)
        
if __name__ == "__main__":
    sensor = TempHumiSensor(4)
    while True:
        print(vars(sensor.read_sensor()))
        time.sleep(0.5)