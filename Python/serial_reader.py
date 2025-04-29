import serial
import time

# Replace 'COM3' with your Arduino COM port (check Arduino IDE)
ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)  # Give time for Arduino to reset

print("Starting to read from Arduino...\n")

while True:
    line = ser.readline().decode('utf-8').strip()
    if line:
        print(line)
