# 🎓 Smart-Learn: Human-Emotion-Aware AI Tutor

An intelligent, closed-loop e-learning ecosystem that uses Edge AI (Computer Vision) to monitor student engagement in real-time. It dynamically adapts digital video content and triggers physical IoT hardware feedback to prevent passive disengagement and cognitive fatigue.

![Project Architecture](https://via.placeholder.com/800x400.png?text=Smart-Learn+Architecture+Diagram) ## 🌟 Core Features

* **Edge AI Perception:** Uses a custom-trained **MobileNetV2** model via OpenCV to classify cognitive states (Focused, Distracted, Confused, Drowsy) in real-time with >70% confidence.
* **Dynamic Video Adaptation:** Automatically pauses video playback during severe drowsiness and triggers a context-aware "Rewind Modal" upon detecting sustained confusion (15+ seconds).
* **Gamified Focus Dashboard:** A responsive HTML/JS UI that tracks engagement via a dynamic "Focus Score" algorithm, including mandatory screen-lock breaks if the score drops below 30%.
* **Physical IoT Proctoring:** Integrates an **ESP8266 NodeMCU** and a 5V relay to trigger a physical DC motor for haptic feedback when critical fatigue is detected.
* **Automated Telegram Analytics:** Compiles session telemetry (duration, score, incident counts) and dispatches asynchronous reports to stakeholders via the Telegram Bot API.

## 🛠️ Technology Stack

* **AI & Computer Vision:** Python 3, TensorFlow/Keras, OpenCV
* **Backend Server:** Java 17, Spring Boot, REST APIs
* **Frontend:** HTML5, JavaScript (DOM Manipulation), Bootstrap 5
* **IoT Hardware:** C++, ESP8266 NodeMCU, 5V Relay, DC Motor
* **Integrations:** Telegram API

## 🚀 How to Run the System

This project requires three separate components running simultaneously over the same Wi-Fi network.

### 1. Start the Java Backend
```bash
cd backend-java/smart-learn
./mvnw spring-boot:run

2. Start the AI Vision Engine
Ensure your webcam is not being used by another application.

Bash

cd ai-engine-python
pip install -r requirements.txt
python test_custom.py

