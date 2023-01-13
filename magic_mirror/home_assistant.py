# Import all the required packages
from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import logging

# Light pin (GPIO channel number)
LIGHT_PIN = 11

# Get light status
def get_light_status():
    # Check current Light status
    GPIO.setup(LIGHT_PIN, GPIO.IN)
    state = GPIO.input(LIGHT_PIN)
    return state

# Light On/off functions
def turn_light_on():
    GPIO.setup(LIGHT_PIN, GPIO.OUT)
    GPIO.output(LIGHT_PIN, GPIO.HIGH)

def turn_light_off():
    GPIO.setup(LIGHT_PIN, GPIO.OUT)
    GPIO.output(LIGHT_PIN, GPIO.LOW)

# Use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)

# Start flask and flask ask
app = Flask(__name__)
ask = Ask(app, '/')

# Let flask ask listen for the 'ExampleIntent
@ask.intent("ChangeLEDStatusIntent")
def gpio_status(status):
    print("Received" + status)

    # Check light status
    state = get_light_status()

    # Want to turn light on?
    if status in ['on','high']:
        # After reading its status we need to set the PIN high again
        turn_light_on()

        # Light is already on
        if (state == True):
            return statement("Light is already on")
        else:
            return statement(f"Turning light {status}")

    # Want to turn light off?
    elif status in ["off", "low"]:
        # Light already off
        if (state == False):
            return statement ("Light is already off")
        else:
            # Turn light off
            turn_light_off()
            return statement (f"Turning light {status}")

if __name__ == "__main__":
    port = 5000 #the custom port vou want
    app.run (host= '127.0.0.1', port=port)
