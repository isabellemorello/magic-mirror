import requests
import json

def app_weather(weather_path):
    APP_ID= "83352619dff682cb26f354f0f60e4d3c"
    latitude = "45.941311"
    longitude = "13.553028"
    endpoint = f"https://api.openweathermap.org/data/2.5/onecall"
    params = {
        "lat" : latitude,
        "lon" : longitude,
        "appid" : APP_ID,
        "exclude" : "minutely,hourly"
    }

    response = requests.get(endpoint, params)
    if response.status_code == 200:
        data = response.json()
        print(data)
        with open(weather_path, "w") as data_file:
            json.dump(data, data_file, indent=4)

if __name__ == "__main__":
    app_weather("../static/weather_one_call.json")