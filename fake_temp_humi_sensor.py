from sensors import ISensor, AReading

class FakeTempHumiditySensor(ISensor): 
    def __init__(self) -> None:
        pass
        

    def read_sensor(self) -> list[AReading]: 
        print(f"The fake sensor is turning ON")
        temperature = -15.0
        humidity = 70.0
        fake_sensor = [temperature, humidity]
        return fake_sensor