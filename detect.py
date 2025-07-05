import cv2
import numpy as np
import os
import pygame
import RPi.GPIO as GPIO
from matplotlib import pyplot as plt

# Initialize pygame mixer
pygame.mixer.init()


# --- GPIO Setup ---
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
button_pin = 7  # Change this if you're using a different pin
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Base project directory
base_dir = "currency_detector_final/currency-detector-opencv-master"
# Path to save captured image
image_path = os.path.join(base_dir, "files", "live_capture.jpg")

# Initialize ORB detector
orb = cv2.ORB_create(nfeatures=1000)

# Training images directory
training_dir = os.path.join(base_dir, "files")

# Load training images
denomination_images = {}
for file in os.listdir(training_dir):
    if file.endswith(".jpg"):
        denom = file.split('_')[0].strip()
        if denom.isdigit():
            if denom not in denomination_images:
                denomination_images[denom] = []
            denomination_images[denom].append(os.path.join(training_dir, file))

print("Loaded denominations:", denomination_images.keys())


def detect_currency():
    test_img = cv2.imread(image_path)
    if test_img is None:
        print("Failed to load captured image")
        return

    kp1, des1 = orb.detectAndCompute(test_img, None)
    if des1 is None:
        print("No keypoints detected in captured image")
        return
    bf = cv2.BFMatcher()
    best_denom = None
    best_avg_score = 0
    best_img_path = None
    best_matches = []
    best_kp2 = []

    for denom, image_paths in denomination_images.items():
        total_matches = 0
        valid_images = 0
        current_best_img_path = None
        current_best_matches = []
        current_best_kp2 = []

        for img_path in image_paths:
            train_img = cv2.imread(img_path)
            kp2, des2 = orb.detectAndCompute(train_img, None)

            if des2 is None:
                continue

            matches = bf.knnMatch(des1, des2, k=2)
            good_matches = [[m] for m, n in matches if m.distance < 0.8 * n.distance]

            print(f"Denomination Rs. {denom} has {len(good_matches)} good matches")
            total_matches += len(good_matches)
            valid_images += 1

            if len(good_matches) > len(current_best_matches):
                current_best_img_path = img_path
                current_best_matches = good_matches
                current_best_kp2 = kp2

        if valid_images > 0:
            avg_score = total_matches / valid_images
            print(f"Denomination Rs. {denom} average good matches: {avg_score:.2f}")

            if avg_score > best_avg_score:
                best_avg_score = avg_score
                best_denom = denom
                best_img_path = current_best_img_path
                best_matches = current_best_matches
                best_kp2 = current_best_kp2

    if best_denom is not None:
        print(f"\nDetected Denomination: Rs. {best_denom} with average good matches: {best_avg_score:.2f}")
        # Play audio
        audio_file = os.path.join(base_dir, "audio", f"{best_denom}.mp3")
        if not os.path.exists(audio_file):
            audio_file = os.path.join(base_dir, "audio", "not_found.mp3")

        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error playing audio: {e}")

        # Show matches
        train_img = cv2.imread(best_img_path)
        img_matches = cv2.drawMatchesKnn(test_img, kp1, train_img, best_kp2, best_matches, None)
        plt.imshow(img_matches)
        plt.title(f"Detected: Rs. {best_denom}")
        plt.axis('off')

    else:
        print("No strong match found.")
        fallback_audio = os.path.join(base_dir, "audio", "not_found.mp3")
        try:
            pygame.mixer.music.load(fallback_audio)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        except Exception as e:
            print(f"Error playing fallback audio: {e}")

def capture_and_process():
    print("Waiting for button press to capture an image...")
    cap = cv2.VideoCapture(1, cv2.CAP_V4L2)  # Use the correct camera index

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        cv2.imshow("Webcam Preview (Press Button to Capture)", frame)

        if GPIO.input(button_pin) == GPIO.LOW:
            print("Button pressed! Capturing image...")
            cv2.imwrite(image_path, frame)
            print("Image captured! Processing...")
            detect_currency()
            break

        if cv2.waitKey(1) & 0xFF == 27:  # ESC key
            break

    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()

# Start
capture_and_process()
