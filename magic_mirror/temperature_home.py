import adafruit_dht
import time
import board
from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import logging

dht_device = adafruit_dht.DHT11(board.D17)


# Read Humidity and Temperature
def read():
    # humidity = None
    temperature = None

    try:
        temperature = dht_device.temperature
        # humidity = dht_device.humidity
        print(f"Temperature is: {temperature}")
        # print(f"Temperature is: {temperature} and Humidity is: {humidity}")

    except RuntimeError as error:
        print(error.args[0])
        print("Temp is None :(")
        time.sleep(2.0)

    except Exception as error:
        dht_device.exit()
        print("DHT killed")
        raise error

    time.sleep(30.0)

    return temperature

app = Flask(__name__)
ask = Ask(app, "/")

@ask.intent("ReadTemperature")
def ask_temperature(temperature):
    print(f"Received {temperature}")

    while True:
        temp = read()

        return statement (f"La temperatura è di {temp}")


if __name__ == '__main__':
    port = 5000
    app.run(host="127.0.0.1", port=port)

    # while True:
    #     humidity, temperature = read()
