import RPi.GPIO as GPIO
import time
import os
import pyttsx3
import subprocess

# GPIO setup for the button
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
button_pin = 7
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"TTS error: {e}")

# Modes and paths
modes = ["face_recognition", "ocr", "currency_detection", "ultrasonic"]
mode_index = 0
button_pressed = False
last_button_state = GPIO.HIGH

mode_files = {
    "face_recognition": "/home/pi/eyeglasses/facerecogwithaudio.py",
    "ocr": "/home/pi/eyeglasses/text-to-speech-final.py",
    "currency_detection": "/home/pi/eyeglasses/currency_detector_final/currency-detector-opencv-master/detetctnew.py",
    "ultrasonic": "/home/pi/eyeglasses/ultrasonic.py"
}

try:
    # Start with face_recognition automatically
    current_mode = modes[mode_index]
    speak(f"Starting with {current_mode.replace('_', ' ')} mode")
    print(f"Starting with: {current_mode}")
    subprocess.run(["python3", mode_files[current_mode]], check=True)

    while True:
        current_button_state = GPIO.input(button_pin)

        if current_button_state == GPIO.LOW and last_button_state == GPIO.HIGH and not button_pressed:
            mode_index = (mode_index + 1) % len(modes)
            current_mode = modes[mode_index]
            print(f"Mode switched to: {current_mode}")
            speak(f"Mode switched to {current_mode.replace('_', ' ')}")
            button_pressed = True
            time.sleep(0.3)  # Debouncing

            # Run the selected mode's script
            script_path = mode_files[current_mode]
            if os.path.exists(script_path):
                try:
                    subprocess.run(["python3", script_path], check=True)
                except subprocess.CalledProcessError as e:
                    print(f"Error running {current_mode}: {e}")
            else:
                print(f"Script not found for mode: {current_mode}")

            # Exit after ultrasonic mode
            if current_mode == "ultrasonic":
                print("Ultrasonic mode completed. Exiting final_code.py.")
                break

        if current_button_state == GPIO.HIGH:
            button_pressed = False

        last_button_state = current_button_state
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Interrupted by user.")
finally:
    GPIO.cleanup()
