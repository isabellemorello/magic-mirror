import adafruit_dht
import time
import board
import json

dht_device = adafruit_dht.DHT11(board.D17)


# Read Humidity and Temperature
def read(temp_path):
    humidity = None
    temperature = None

    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print(f"Temperature is: {temperature}° and Humidity is: {humidity}%")

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)

    except Exception as error:
        dht_device.exit()
        print("DHT killed")
        raise error

    with open(temp_path, "w") as temp:
        json.dump(temperature, temp, indent=4)

    # time.sleep(30.0)

    # return humidity, temperature
    return temperature

if __name__ == '__main__':
    # while True:
    temperature = read("static/temperature.json")
    print(temperature)
    # humidity, temperature = read("static/temperature.json")
