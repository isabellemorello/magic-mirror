import json
import math

class Weather:
    def __init__(self, weather_data):
        self.current = self.get_current_weather(weather_data)
        self.icon = self.get_icon(weather_data)
        self.temperature = self.get_temperature(weather_data)
        self.daily_icon = self.get_daily_icon(weather_data)
        self.daily_max_min = self.get_daily_max_min(weather_data)

    def get_data(self, weather_data):
        with open(weather_data, "r") as data_file:
            data = json.load(data_file)
        # print(data)
        return data

    def get_current_weather(self, weather_data):
        data = self.get_data(weather_data)
        current_weather = data["current"]["weather"][0]["description"]
        # print(current_weather)
        return current_weather

    def get_icon(self, weather_data):
        data = self.get_data(weather_data)
        icon = data["current"]["weather"][0]["icon"]
        # print(icon)
        return icon

    def get_temperature(self, weather_data):
        data = self.get_data(weather_data)
        temp = data["current"]["temp"]
        temp_celsius = math.floor(temp - 273.15)
        # print(temp_celsius)
        return temp_celsius


    def get_daily_icon(self, weather_data):
        data = self.get_data(weather_data)
        daily = data["daily"]
        icons = [day["weather"][0]["icon"] for day in daily]
        # print(icons)
        return icons

    def get_daily_max_min(self, weather_data):
        data = self.get_data(weather_data)
        daily = data["daily"]
        max_min = [(math.floor(day["temp"]["max"] - 273.15), math.floor(day["temp"]["min"] - 273.15)) for day in daily]
        # print(max_min)
        return max_min

# w = Weather()
# current = w.daily_max_min