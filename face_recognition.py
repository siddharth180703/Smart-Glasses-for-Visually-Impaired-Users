import cv2
import numpy as np
import os
import pyttsx3
import time

# Initialize speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def text_to_speech(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Text-to-speech error: {e}")

# Paths
haar_file = '/home/pi/eyeglasses/myfacerecognizer/haarcascade_frontalface_default.xml'
datasets = '/home/pi/eyeglasses/myfacerecognizer/datasets'

# Prepare training data
print('Recognizing Face. Please ensure sufficient lighting...')
(images, labels, names, id) = ([], [], {}, 0)

for (subdirs, dirs, files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets, subdir)
        for filename in os.listdir(subjectpath):
            path = os.path.join(subjectpath, filename)
            images.append(cv2.imread(path, 0))
            labels.append(id)
        id += 1

(width, height) = (130, 100)
(images, labels) = [np.array(lis) for lis in [images, labels]]

# Train the model
model = cv2.face.LBPHFaceRecognizer_create()
model.train(images, labels)

# Load face cascade
face_cascade = cv2.CascadeClassifier(haar_file)

# Start camera (0 for Pi camera via V4L2)
webcam = cv2.VideoCapture(1)
if not webcam.isOpened():
    print("Error: Could not open webcam.")
    exit()

start_time = time.time()
detection_timeout = 10  # seconds

while True:
    ret, im = webcam.read()
    if not ret:
        print("Failed to grab frame.")
        break

    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            face = gray[y:y + h, x:x + w]
            face_resize = cv2.resize(face, (width, height))
            prediction = model.predict(face_resize)

            if prediction[1] < 500:
                predicted_name = names[prediction[0]]
                confidence = prediction[1]

                if confidence > 50:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(im, f'{predicted_name} - {confidence:.0f}', (x - 10, y - 10),
                                cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                    print(f"Recognized: {predicted_name}")
                    time.sleep(2)
                    text_to_speech(f"{predicted_name} recognized")
                    break  # Exit loop after recognition
            else:
                cv2.putText(im, 'Not recognized', (x - 10, y - 10),
                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        else:
            continue  # Keep looping if no confident recognition
        break  # Exit outer loop once face is recognized
    else:
        if time.time() - start_time > detection_timeout:
            text_to_speech("No face detected")
            print("No face detected.")
            break
        else:
            cv2.putText(im, 'No face detected', (50, 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)

    cv2.imshow('Face Recognition', im)
    if cv2.waitKey(10) == 27:  # ESC key
        break

# Cleanup
webcam.release()
cv2.destroyAllWindows()
