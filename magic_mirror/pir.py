import RPi.GPIO as GPIO
import time

def motion_pir():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    PIR_PIN = 4 # Assign GPIO4 pin 7 to PIR
    GPIO.setup(PIR_PIN, GPIO.IN) # Setup GPIO pin PIR as input

    print('Sensor initializing . . .')

    time.sleep(60) # Give sensor time to start-up, 60 seconds print('Active')

    def pir(pin):
        print('Movimento Rilevato!')


    GPIO.add_event_detect(4, GPIO.FALLING, callback=pir, bouncetime=100)
    print('[Clicca Ctrl + C per terminare il programma!]')
    try:
        while True:
            time.sleep(0.001)
    except KeyboardInterrupt:
        print('\nScript ended')
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    motion_pir()