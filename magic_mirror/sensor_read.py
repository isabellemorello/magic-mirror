import adafruit_dht
import time
import board

dht_device = adafruit_dht.DHT11(board.D17)


# Read Humidity and Temperature
def read():
    humidity = None
    temperature = None

    try:
        temperature = dht_device.temperature
        humidity = dht_device.humidity
        print(f"Temperature is: {temperature} and Humidity is: {humidity}")

    except RuntimeError as error:
        print(error.args[0])
        time.sleep(2.0)

    except Exception as error:
        dht_device.exit()
        print("DHT killed")
        raise error

    time.sleep(30.0)

    return humidity, temperature


if __name__ == '__main__':
    while True:
        humidity, temperature = read()
