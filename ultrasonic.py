import RPi.GPIO as GPIO
import time
from gtts import gTTS
import os

# Use physical pin numbers
GPIO.setmode(GPIO.BOARD)

TRIG = 8    # Board pin 8
ECHO = 10   # Board pin 10
BUTTON = 7  # Board pin 7

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(TRIG, GPIO.LOW)
time.sleep(2)

def speak_distance(dist):
    text = f"Object is {int(dist)} centimeters away"
    tts = gTTS(text=text, lang='en')
    tts.save("/tmp/distance.mp3")
    os.system("mpg123 /tmp/distance.mp3")

last_time_spoken = 0
speak_delay = 3

try:
    while True:
        # ?? Exit if button is pressed
        if GPIO.input(BUTTON) == GPIO.LOW:
            print("Toggle button pressed. Exiting program.")
            break

        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO) == 0:
            pulse_start = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = round(pulse_duration * 17150, 2)

        print(f"Distance: {distance} cm")

        if distance < 75 and time.time() - last_time_spoken > speak_delay:
            speak_distance(distance)
            last_time_spoken = time.time()
        time.sleep(0.3)

except KeyboardInterrupt:
    print("Keyboard interrupt")

finally:
    GPIO.cleanup()
    print("GPIO cleaned up.")