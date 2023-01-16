import adafruit_dht
import board
from sensor_read import read as read_temp
from flask import Flask
from flask_ask import Ask, statement, convert_errors

dht_device = adafruit_dht.DHT11(board.D17)


temp = None

app = Flask(__name__)
ask = Ask(app, "/")

@ask.intent("ReadTemperature")
def ask_temperature(temperature):
    print(f"Received {temperature}")

    if temperature in ["temperatura"]:
        global temp
        while temp == None:
            temp = read_temp("static/temperature.json")

        return statement (f"La temperatura è di {temp} gradi")


if __name__ == '__main__':
    port = 5000
    app.run(host="127.0.0.1", port=port)
