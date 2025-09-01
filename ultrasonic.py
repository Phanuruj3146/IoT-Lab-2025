import RPi.GPIO as GPIO
import time

# Define GPIO pins
TRIG = 23   # Trig pin connected to GPIO7
ECHO = 24   # Echo pin connected to GPIO11

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    print("Ultrasonic Sensor Setup Complete")
    time.sleep(2)

def get_distance():
    # Send 10us pulse to TRIG
    GPIO.output(TRIG, True)
    time.sleep(0.00001)  # 10µs
    GPIO.output(TRIG, False)

    # Wait for ECHO to go HIGH
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for ECHO to go LOW
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculate pulse duration
    pulse_duration = pulse_end - pulse_start

    # Distance = (time * speed of sound) / 2
    distance = pulse_duration * 34300 / 2  # in cm
    return round(distance, 2)

def loop():
    try:
        while True:
            dist = get_distance()
            print("Distance: {} cm".format(dist))
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMeasurement stopped by user")
        GPIO.cleanup()

if __name__ == "__main__":
    setup()
    loop()
