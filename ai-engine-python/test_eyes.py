import cv2
import requests
import time

# --- CONFIGURATION ---
JAVA_URL = "http://localhost:8080/api/update"
# Put your NodeMCU IP here
NODEMCU_IP = "192.168.1.105" 
HARDWARE_URL = f"http://{NODEMCU_IP}/set"

# --- LOAD DETECTORS (Standard OpenCV) ---
# We use the pre-installed classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# This detects open eyes. If it sees no eyes, you are sleeping.
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Camera Setup
cap = cv2.VideoCapture(0)

# Variables
closed_frames = 0
last_status = "READY"

print("--- Lightweight Eye Tracker Active ---")

while True:
    ret, frame = cap.read()
    if not ret: break

    # Convert to Grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 1. Detect Face
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    current_status = "BORED" # Default (No face = Bored)

    for (x, y, w, h) in faces:
        current_status = "FOCUSED"
        
        # Draw box around face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # 2. Look for Eyes INSIDE the face area only
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        
        # Detect Eyes
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 4)
        
        # 3. LOGIC: If face is there, but NO eyes detected -> Sleeping
        if len(eyes) == 0:
            closed_frames += 1
            if closed_frames > 10: # If eyes missing for ~0.5 seconds
                current_status = "SLEEPING"
        else:
            closed_frames = 0 # Eyes found! Reset counter.
            
            # Draw circles around eyes to show it's working
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    # --- SEND TO JAVA / IOT ---
    if current_status != last_status:
        print(f"Status Change: {current_status}")
        try:
            requests.get(JAVA_URL, params={'status': current_status}, timeout=0.1)
            # requests.get(HARDWARE_URL, params={'status': current_status}, timeout=0.1)
        except:
            pass
        last_status = current_status

    # UI Display
    color = (0, 255, 0)
    if current_status == "SLEEPING": 
        color = (0, 0, 255)
        cv2.putText(frame, "WAKE UP!", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)
    elif current_status == "BORED": 
        color = (0, 165, 255)

    cv2.putText(frame, f"STATUS: {current_status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow("Lightweight Tracker", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()