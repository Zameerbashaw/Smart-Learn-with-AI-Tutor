

import cv2
import numpy as np
import os

# --- 1. FORCE LEGACY COMPATIBILITY ---
os.environ["TF_USE_LEGACY_KERAS"] = "1"

# --- 2. USE THE COMPATIBILITY LIBRARY ---
import tf_keras as keras
import requests

# --- CONFIGURATION ---
JAVA_URL = "http://localhost:8080/api/update"

# Make sure this is the EXACT IP showing on your NodeMCU Serial Monitor today!
# Mobile hotspots like your "Moto g62" change this IP every time you turn them on.
# NODEMCU_IP = "192.168.1.105" 
NODEMCU_IP = "10.193.229.161" 
HARDWARE_URL = f"http://{NODEMCU_IP}/set"

# --- LOAD THE BRAIN ---
print("Loading Custom AI Model... (Using Legacy Adapter)")

# We load using the legacy library
model = keras.models.load_model("keras_model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()
print("Model Loaded Successfully!")

# Setup Camera
cap = cv2.VideoCapture(0)
last_status = "INIT"

print("--- Custom AI Tutor Active ---")

while True:
    ret, frame = cap.read()
    if not ret: break

    # 1. PREPARE IMAGE
    # Resize to 224x224 pixels (Standard for Teachable Machine)
    image = cv2.resize(frame, (224, 224), interpolation=cv2.INTER_AREA)
    # Make it a numpy array
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    # Normalize colors (Make them between -1 and 1)
    image = (image / 127.5) - 1

    # 2. PREDICT
    try:
        prediction = model.predict(image, verbose=0)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # Clean the text (Remove numbers like "0 FOCUSED")
        current_status = class_name[2:].strip()

        # 3. LOGIC (Only trust if > 70% sure)
        if confidence_score > 0.70:
            
            # Display Colors
            color = (0, 255, 0) # Green
            if current_status == "SLEEPING": color = (0, 0, 255) # Red
            elif current_status == "BORED": color = (0, 165, 255) # Orange
            elif current_status == "CONFUSED": color = (0, 255, 255) # Yellow

            # Draw UI
            cv2.putText(frame, f"STATUS: {current_status}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            cv2.putText(frame, f"Conf: {str(int(confidence_score*100))}%", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1)

            # 4. SEND TO JAVA / IOT
            if current_status != last_status:
                print(f"State Change: {current_status}")
                try:
                    # 1. Send to the Website
                    requests.get(JAVA_URL, params={'status': current_status}, timeout=0.1)
                    
                    # 2. Send to the NodeMCU (THIS WAS MISSING!)
                    requests.get(HARDWARE_URL, params={'status': current_status}, timeout=0.1)
                except Exception as req_e:
                    # Silently pass if the network is too slow so the video doesn't lag
                    pass
                last_status = current_status

    except Exception as e:
        print(f"Prediction Error: {e}")

    cv2.imshow('Custom AI Tutor', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()