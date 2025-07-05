import cv2
import pytesseract
from gtts import gTTS
import pygame
import time
import os
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

# --- GPIO Setup ---
button_pin = 7  # Button connected to GPIO pin 7
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up the button pin as input with pull-up

# --- Format text for speech ---
def format_text_for_speech(text):
    text = text.replace(",", " , ")
    text = text.replace(".", " . ")
    text = text.replace("?", " ? ")
    text = text.replace("!", " ! ")
    return text.strip()

# --- Human-like TTS using Google Text-to-Speech ---
def text_to_speech(text):
    tts = gTTS(text=text, lang='en', slow=False)
    filename = "output.mp3"
    tts.save(filename)

    # Initialize the mixer and play audio
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait for the audio to finish
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    os.remove(filename)  # Clean up the file after playing

# --- Live webcam preview and capture on button press ---
def capture_on_button_press(camera_index=1):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("? Failed to open webcam.")
        return None

    print("?? Press button to capture, or ESC to exit.")

    # Create the window only once
    window_name = "Live Webcam - Press Button to Capture"

    while True:
        ret, frame = cap.read()
        if not ret:
            print("? Failed to read frame.")
            break

        # Show live feed
        cv2.imshow(window_name, frame)

        # Wait for GPIO button press
        if GPIO.input(button_pin) == GPIO.LOW:  # Button pressed (LOW indicates press for pull-up configuration)
            print("?? Button pressed. Captured frame.")
            cv2.imwrite("captured_image.jpg", frame)  # Save the captured image
            cap.release()  # Release the camera
            cv2.destroyAllWindows()  # Close the preview window immediately after capture
            return frame

        # Check for ESC key to exit
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            print("? Exiting.")
            cap.release()
            cv2.destroyAllWindows()  # Close the preview window
            return None

# --- OCR Process ---
def perform_ocr(image):
    # Preprocess for OCR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Show preprocessed image
    plt.imshow(gray, cmap='gray')
    plt.title("Captured Image")
    plt.axis('off')

    # OCR
    print("?? Performing OCR...")
    text = pytesseract.image_to_string(gray)

    # Format and speak
    processed_text = format_text_for_speech(text)
    print("?? Extracted Text:\n", processed_text)

    if processed_text.strip():
        with open("output.txt", "w") as f:
            f.write(processed_text)
        text_to_speech(processed_text)
    else:
        print("?? No text detected.")

# --- Main ---
image = capture_on_button_press()

if image is None:
    print("No image captured.")
    exit()

# Perform OCR after capturing the image
perform_ocr(image)

# Clean up GPIO at the end
GPIO.cleanup()
