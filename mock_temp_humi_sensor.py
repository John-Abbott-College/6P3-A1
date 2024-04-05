from sensors import ISensor, AReading

class MockTempHumiditySensor(ISensor): 
    def __init__(self) -> None:
        

    def read_sensor(self) -> list[AReading]: 
        print(f"The mock sensor is turning ON")
        temperature = -15.0
        humidity = 70.0
        fake_sensor = [temperature, humidity]
        return fake_sensor