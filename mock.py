import random
from time import sleep

class MockDeviceController:
    def __init__(self):
        pass

    def run(self):
        """Runs the device in development mode."""
        while True:
            fan_value = random.choice(["ON", "OFF"])
            led_value = random.choice(["ON", "OFF"])

            print(f"Fan is {fan_value}")
            print(f"LED is {led_value}")
           
            temperature = round(random.uniform(20, 30), 2)
            humidity = round(random.uniform(40, 60), 2)

            print(f"Temperature: {temperature}°C, Humidity: {humidity}%")

            sleep(2)