import RPi.GPIO as GPIO
import time

# Pin setup
LED_PIN = 27   # Change this to the GPIO pin where your LED is connected
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn LED on
        print("LED ON")
        time.sleep(1)  # Keep it on for 1 second

        GPIO.output(LED_PIN, GPIO.LOW)   # Turn LED off
        print("LED OFF")
        time.sleep(1)  # Keep it off for 1 second

except KeyboardInterrupt:
    print("Program stopped")

finally:
    GPIO.cleanup()
