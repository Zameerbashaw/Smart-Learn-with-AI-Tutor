import cv2
import requests
import time

# --- CONFIGURATION ---
# 1. Java Dashboard (Localhost)
JAVA_URL = "http://localhost:8080/api/update"

# 2. NodeMCU Hardware
# CHECK THIS IP! Use the one you wrote down earlier.
NODEMCU_IP = "10.51.125.161"

 
HARDWARE_URL = f"http://{NODEMCU_IP}/set"

# Setup Camera
cap = cv2.VideoCapture(0)
# Load the face detector (Make sure the XML file is not needed in the folder, this uses the internal one)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

last_status = "READY"
print(f"--- AI Tutor Active ---")
print(f"Connecting to Hardware at: {HARDWARE_URL}")

while True:
    ret, frame = cap.read()
    if not ret: break

    # Convert to grayscale for detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Default logic: If no face is seen, student is BORED
    current_status = "BORED"

    # If a face IS seen, student is FOCUSED
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        current_status = "FOCUSED"

    # SEND UPDATE ONLY IF STATUS CHANGES (To prevent lagging)
    if current_status != last_status:
        print(f"Status Change: {current_status}")
        
        # 1. Send to Java Website
        try:
            requests.get(JAVA_URL, params={'status': current_status}, timeout=0.1)
        except:
            pass # Ignore if Java is slow

        # 2. Send to NodeMCU (The Hardware)
        try:
            requests.get(HARDWARE_URL, params={'status': current_status}, timeout=0.2)
            print(f"Signal sent to NodeMCU: {current_status}")
        except:
            pass 

        last_status = current_status

    # Show the video feed
    color = (0, 255, 0) if current_status == "FOCUSED" else (0, 165, 255)
    cv2.putText(frame, f"STATUS: {current_status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.imshow('AI Tutor', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()