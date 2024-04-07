from sensors import ISensor, AReading

class MockTempHumiditySensor(ISensor):
    def __init__(self, address: hex = 0x38, bus: int = 4, model: str = "", type: AReading = AReading) -> None:
        self._sensor_model = model
        self.reading_type = type

    def read_sensor(self) -> list[AReading]:
        temperature = 25.0  
        humidity = 50.0  
        print(f'Mock Temperature in Celsius is {temperature} C')
        print(f'Mock Relative Humidity is {humidity} %')
        return [temperature, humidity]

# Test the MockTempHumiditySensor
def main():
    sensor = MockTempHumiditySensor()
    while True:
        sensor.read_sensor()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
