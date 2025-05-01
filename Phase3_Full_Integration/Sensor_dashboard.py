import serial
import time
import matplotlib.pyplot as plt
from collections import deque

# ——— CONFIG ———
PORT        = 'COM4'
BAUD        = 9600
TIMEOUT     = 1
WINDOW_SIZE = 100

# ——— SERIAL SETUP ———
ser = serial.Serial(PORT, BAUD, timeout=TIMEOUT)
time.sleep(2)  # allow Arduino reset

# ——— DATA BUFFERS ———
t_buf  = deque(maxlen=WINDOW_SIZE)
d_buf  = deque(maxlen=WINDOW_SIZE)
ax_buf = deque(maxlen=WINDOW_SIZE)
ay_buf = deque(maxlen=WINDOW_SIZE)
az_buf = deque(maxlen=WINDOW_SIZE)
gx_buf = deque(maxlen=WINDOW_SIZE)
gy_buf = deque(maxlen=WINDOW_SIZE)
gz_buf = deque(maxlen=WINDOW_SIZE)
btn_buf= deque(maxlen=WINDOW_SIZE)

start = time.time()

# ——— PLOT SETUP ———
plt.ion()
fig, axs = plt.subplots(4, 1, figsize=(10, 9), sharex=True)
axs[0].set_title("Distance (cm)")
axs[1].set_title("Accel (ax, ay, az)")
axs[2].set_title("Gyro (gx, gy, gz)")
axs[3].set_title("Button State (1=Pressed)")
axs[3].set_ylim(-0.1, 1.1)
axs[3].set_xlabel("Time (s)")

print("Starting multi-sensor + button dashboard…\n")

try:
    while True:
        raw = ser.readline().decode('utf-8', 'ignore').strip()
        if not raw:
            continue

        parts = raw.split(',')
        # we now expect 8 parts
        if len(parts) != 8:
            continue

        try:
            dist   = float(parts[0])
            ax, ay, az = map(int, parts[1:4])
            gx, gy, gz = map(int, parts[4:7])
            btn    = int(parts[7])
        except ValueError:
            continue

        # ignore out-of-range
        if dist < 0 or dist > 200:
            continue

        t = time.time() - start

        # append
        t_buf.append(t)
        d_buf.append(dist)
        ax_buf.append(ax); ay_buf.append(ay); az_buf.append(az)
        gx_buf.append(gx); gy_buf.append(gy); gz_buf.append(gz)
        btn_buf.append(btn)

        # clear & plot
        axs[0].clear()
        axs[0].plot(t_buf, d_buf, label='Distance')
        axs[0].set_ylabel("cm")
        axs[0].legend(loc='upper right')

        axs[1].clear()
        axs[1].plot(t_buf, ax_buf, label='Ax')
        axs[1].plot(t_buf, ay_buf, label='Ay')
        axs[1].plot(t_buf, az_buf, label='Az')
        axs[1].set_ylabel("Accel")
        axs[1].legend(loc='upper right')

        axs[2].clear()
        axs[2].plot(t_buf, gx_buf, label='Gx')
        axs[2].plot(t_buf, gy_buf, label='Gy')
        axs[2].plot(t_buf, gz_buf, label='Gz')
        axs[2].set_ylabel("Gyro")
        axs[2].legend(loc='upper right')

        axs[3].clear()
        axs[3].plot(t_buf, btn_buf, drawstyle='steps-post', label='Button')
        axs[3].set_ylabel("State")
        axs[3].legend(loc='upper right')

        # simple alerts
        if dist < 20:
            print(f"⚠️ ALERT @ {t:.1f}s — Distance < 20 cm ({dist:.1f} cm)")
        if btn == 1:
            print(f"🔘 BUTTON PRESSED @ {t:.1f}s")

        plt.pause(0.05)

except KeyboardInterrupt:
    print("\nDashboard stopped by user.")
finally:
    ser.close()
