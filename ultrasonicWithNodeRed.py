import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import threading

# ---------------- GPIO Pins ----------------
TRIG = 4
ECHO = 17

# ---------------- MQTT Settings ----------------
BROKER = "broker.hivemq.com"  # Public broker
PORT = 1883
TOPIC_CONTROL = "ultrasonic/control"
TOPIC_DATA = "ultrasonic/data"

running = False  # Flag for sensor loop

# ---------------- GPIO Setup ----------------
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

# ---------------- Ultrasonic Function ----------------
def get_distance():
    # Trigger ultrasonic
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = None
    pulse_end = None

    # Wait for echo start
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    # Wait for echo end
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    if pulse_start and pulse_end:
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 34300 / 2
        return round(distance, 2)
    else:
        return None

# ---------------- Sensor Loop ----------------
def sensor_loop(client):
    global running
    while running:
        dist = get_distance()
        if dist is not None:
            client.publish(TOPIC_DATA, str(dist))
            print("Distance:", dist, "cm")
        else:
            client.publish(TOPIC_DATA, "No Reading")
            print("No Reading")
        time.sleep(1)

# ---------------- MQTT Callbacks ----------------
def on_connect(client, userdata, flags, rc):
    print("Connected with result code", rc)
    client.subscribe(TOPIC_CONTROL)

def on_message(client, userdata, msg):
    global running
    payload = msg.payload.decode()
    print("Received:", payload)

    if payload == "ON" and not running:
        running = True
        threading.Thread(target=sensor_loop, args=(client,), daemon=True).start()
    elif payload == "OFF":
        running = False

# ---------------- MQTT Setup ----------------
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)

# ---------------- Main ----------------
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    GPIO.cleanup()
