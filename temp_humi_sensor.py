from time import sleep
from sensors import ISensor, AReading


class TempHumiditySensor(ISensor): 
    def __init__(self, model:str, type:AReading.Type) -> None:
        self._sensor_model = model
        self.reading_type = type

        self.counter = 1.00
        self.max_count = 120.00

    #Placeholder data to return
    def read_sensor(self) -> list[AReading]:
        self.counter += 0.05 if self.counter < self.max_count else 1.00

        return [
            AReading(AReading.Type.TEMPERATURE, AReading.Unit.CELCIUS, 25.00 + self.counter),
            AReading(AReading.Type.HUMIDITY, AReading.Unit.HUMIDITY, self.counter/10)
        ]

    

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
