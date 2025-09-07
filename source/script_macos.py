import sys
import time
import serial
import serial.tools.list_ports
import numpy as np
from PIL import ImageGrab, Image

# ==== CONFIG ====
BAUD_RATE = 460800  # MUST MATCH WITH THE .INO SCRIPT
FPS = 30
OLED_WIDTH = 128
OLED_HEIGHT = 64

# Capture area: None = full screen, or set (left, top, right, bottom)
CROP_BOX = None  # e.g., (0, 50, 480, 240)

# ==== SERIAL PORT CHOOSER ====
print("Available serial ports:")
ports = list(serial.tools.list_ports.comports())
if not ports:
    print("No serial ports found! Please connect your ESP32.")
    sys.exit(1)

for i, port in enumerate(ports):
    print(f"[{i}] {port.device} - {port.description}")

choice = input("Select port number: ").strip()
try:
    choice = int(choice)
    SERIAL_PORT = ports[choice].device
except (ValueError, IndexError):
    print("Invalid choice.")
    sys.exit(1)

# ==== SERIAL SETUP ====
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)
print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

# ==== IMAGE PROCESSING ====
def preprocess_image(img):
    img = img.convert("L")  # grayscale
    img = img.resize((OLED_WIDTH, OLED_HEIGHT), Image.NEAREST)
    img = img.convert("1", dither=Image.FLOYDSTEINBERG)  # 1-bit with dithering
    return img

# ==== MAIN LOOP ====
frame_time = 1 / FPS

try:
    while True:
        start = time.perf_counter()

        img = ImageGrab.grab(bbox=CROP_BOX)
        img = preprocess_image(img)

        arr = np.array(img, dtype=np.uint8)
        data = np.packbits(arr, axis=1).tobytes()

        # optional sync marker (like in your first script)
        # ser.write(b"\xAA")
        ser.write(data)

        elapsed = time.perf_counter() - start
        time.sleep(max(0, frame_time - elapsed))

except KeyboardInterrupt:
    ser.close()
    print("Stopped streaming")
