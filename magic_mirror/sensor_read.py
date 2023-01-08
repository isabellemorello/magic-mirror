import adafruit_dht
import time
import board

# NB: questo è il numero della GPIO, non il numero fisico della board
dht_device = adafruit_dht.DHT11(board.D17)

# Read Humidity and Temperature
def read():

    humidity = None
    temperature = None

    try:
        #Try read from the sensor
        temperature = dht_device.temperature
        humidity = dht_device.humidity

    except RuntimeError as error:
        #GLi errori capitano piuttosto spesso
        print(error.args[0])
        time.sleep(1.0)

    except Exception as error:
        dht_device.exit()
        print("DHT killed")
        raise error

    return humidity, temperature

if __name__ == '__main__':
    while True:
        humidity, temperature = read()

        if humidity is not None and temperature is not None: