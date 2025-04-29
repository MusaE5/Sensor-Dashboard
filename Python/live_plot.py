import serial
import time
import matplotlib.pyplot as plt
from collections import deque

# ——— CONFIG ———
PORT = 'COM4'
BAUD = 9600
TIMEOUT = 1
WINDOW_SIZE = 100  # how many points to show per plot

# ——— SERIAL SETUP ———
ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
time.sleep(2)

# ——— DATA BUFFERS ———
time_data = deque(maxlen=WINDOW_SIZE)
distance_data = deque(maxlen=WINDOW_SIZE)
ax_data = deque(maxlen=WINDOW_SIZE)
ay_data = deque(maxlen=WINDOW_SIZE)
az_data = deque(maxlen=WINDOW_SIZE)
gx_data = deque(maxlen=WINDOW_SIZE)
gy_data = deque(maxlen=WINDOW_SIZE)
gz_data = deque(maxlen=WINDOW_SIZE)

start_time = time.time()

# ——— PLOT SETUP ———
plt.ion()
fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
axs[0].set_title("Distance (cm)")
axs[1].set_title("Accelerometer (ax, ay, az)")
axs[2].set_title("Gyroscope (gx, gy, gz)")
axs[2].set_xlabel("Time (s)")

print("Starting multi-sensor dashboard...\n")

# ——— MAIN LOOP ———
try:
    while True:
        raw = ser.readline().decode('utf-8', errors='ignore').strip()
        if not raw:
            continue

        parts = raw.split(',')
        if len(parts) != 7:
            continue

        try:
            dist = float(parts[0])
            ax = int(parts[1])
            ay = int(parts[2])
            az = int(parts[3])
            gx = int(parts[4])
            gy = int(parts[5])
            gz = int(parts[6])
        except ValueError:
            continue

        # Filter bad data
        if dist < 0 or dist > 200:
            continue

        t = time.time() - start_time

        # Append to buffers
        time_data.append(t)
        distance_data.append(dist)
        ax_data.append(ax)
        ay_data.append(ay)
        az_data.append(az)
        gx_data.append(gx)
        gy_data.append(gy)
        gz_data.append(gz)

        # ——— PLOTTING ———
        axs[0].clear()
        axs[0].plot(time_data, distance_data, label='Distance', color='blue')
        axs[0].set_ylabel("cm")
        axs[0].legend()

        axs[1].clear()
        axs[1].plot(time_data, ax_data, label='Ax')
        axs[1].plot(time_data, ay_data, label='Ay')
        axs[1].plot(time_data, az_data, label='Az')
        axs[1].set_ylabel("Accel")
        axs[1].legend()

        axs[2].clear()
        axs[2].plot(time_data, gx_data, label='Gx')
        axs[2].plot(time_data, gy_data, label='Gy')
        axs[2].plot(time_data, gz_data, label='Gz')
        axs[2].set_ylabel("Gyro")
        axs[2].legend()

        for ax in axs:
            ax.relim()
            ax.autoscale_view()

        plt.pause(0.05)

except KeyboardInterrupt:
    print("\nDashboard stopped.")
finally:
    ser.close()
