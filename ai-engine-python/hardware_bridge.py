import serial
import time

# 1. SETUP THE CONNECTION
# Make sure 'COM8' matches what you see in the Arduino IDE
try:
    ser = serial.Serial('COM8', 115200, timeout=1)
    print("Connected to NodeMCU on COM8")
except:
    print("Error: Could not connect. Check if the Serial Monitor is still open!")

def send_status_to_tutor(status_char):
    """
    Sends 'A' (Attentive), 'F' (Frustrated), or 'B' (Bored) to NodeMCU
    """
    if ser.is_open:
        ser.write(status_char.encode())
        print(f"Sent {status_char} to Hardware")

# 2. TEST LOOP (Replace this with your AI detection logic later)
try:
    while True:
        # Example: Simulating AI detection
        send_status_to_tutor('A') # Tell hardware student is Attentive
        time.sleep(5)
        send_status_to_tutor('F') # Tell hardware student is Frustrated
        time.sleep(5)
except KeyboardInterrupt:
    ser.close()
    print("Connection closed.")