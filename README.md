# 🕶️ Smart Glasses for Visually Impaired Users

An AI-powered wearable assistive device built to empower visually impaired individuals with real-time environment awareness, currency identification, face recognition, and text reading capabilities.

## 🚀 Overview

Smart Glasses is a Raspberry Pi-based portable device integrated with various deep learning models and sensors to assist visually impaired users in everyday tasks. The device provides audio feedback using Text-to-Speech (TTS) and can recognize faces, detect objects, identify currency denominations, and read printed text from the surroundings.

---

## 🧠 Features

### 🔎 Face Recognition

- Users can upload known faces to the device.
- The system uses **FaceNet** to match detected faces with stored ones.
- Provides **real-time audio feedback** about recognized individuals.

### 💵 Currency Detection

- Trained a custom CNN model on various Indian currency denominations.
- Users upload a dataset of currency images, and the model is trained locally.
- Device identifies currency via camera and announces denomination using TTS.

### 🧱 Object Detection with Ultrasonic Sensors

- Uses **ultrasonic sensors** to detect nearby obstacles.
- Provides vibration feedback and/or voice alerts to warn users.

### 📖 Text Reading (OCR)

- Uses **DOCTR OCR** and OpenCV to extract printed or handwritten text.
- Converts extracted text to speech using TTS for real-time reading.

---

## 🔐 AI Models Used

| Feature            | Model Used                                        | Type                              |
| ------------------ | ------------------------------------------------- | --------------------------------- |
| Face Recognition   | FaceNet                                           | Deep Metric Learning              |
| Currency Detection | Custom CNN model (trained using Keras/TensorFlow) | Image Classification              |
| Object Detection   | YOLOv5 / Ultrasonic Sensors                       | Real-time detection + sensor data |
| Text Reading       | DOCTR OCR + OpenCV                                | Text Extraction                   |

> 🧠 Note: All models were trained or fine-tuned by the team using custom datasets.

---

## 🛠️ Tech Stack

| Component              | Technology Used                                   |
| ---------------------- | ------------------------------------------------- |
| Hardware               | Raspberry Pi 4, Camera Module, Ultrasonic Sensors |
| AI/ML Frameworks       | TensorFlow, Keras, PyTorch                        |
| OCR & Image Processing | OpenCV, DOCTR OCR                                 |
| TTS Engine             | pyttsx3 / Google Text-to-Speech                   |
| Languages              | Python                                            |
| Storage                | Local storage (trained models, faces, datasets)   |

---

## 🎯 Project Highlights

- 🧠 Locally trained AI models for currency and face recognition.
- 🔄 Real-time integration of camera feed with TTS response.
- 📁 Modular and extensible codebase for easy feature addition.
- 🎯 Focused on real-world impact and usability.

---

## 🧪 Challenges Faced & Solutions

- **Challenge**: Integrating multiple AI models with limited hardware (Raspberry Pi).

  - ✅ **Optimized models** for edge devices using quantization and minimal dependencies.

- **Challenge**: Coordinating team contributions across hardware and AI modules.

  - ✅ **Divided work based on skill** (AI, hardware, software), maintained shared Git repo and used Trello/Notion for updates.

- **Challenge**: Real-time TTS delay.
  - ✅ Used lightweight engines like `pyttsx3` and batch processing of OCR text.

---

## 👨‍💻 Team Collaboration

- 👨‍💻 AI/ML: Currency classification, FaceNet training, OCR integration.
- 🤖 Hardware: Sensor wiring, camera setup, Raspberry Pi config.
- 🧩 Integration: UI flow, TTS connection, real-time stream logic.

---

## 📌 Future Improvements

- 🔄 Add multilingual TTS support (Hindi, regional languages).
- 📶 Add mobile sync / Bluetooth notifications.
- 🧠 Integrate Navigation/GPS module for outdoor assistance.

---

## 📽️ Demo

> 📹 Photos, Report and Project Presentation attached for the reference.

---

## 🤝 Acknowledgments

- **FaceNet** – Deep face recognition model.
- **YOLO** – Object detection inspiration.
- **TTS / OCR** – Open-source communities for accessible AI.

---

## 🧾 License

This project is for educational and research purposes only.
