import serial
import time
from PIL import ImageGrab, Image
import numpy as np

# ==== CONFIG ====
SERIAL_PORT = "/dev/tty.SLAB_USBtoUART"
BAUD_RATE = 460800  # MAKE SURE TO MATCH WITH THE .INO SCRIPT
FPS = 30
OLED_WIDTH = 128
OLED_HEIGHT = 64

# Capture area: None = full screen, or set (left, top, right, bottom)
CROP_BOX = None  # e.g., (0, 50, 480, 240)

# ==== SERIAL SETUP ====
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

def preprocess_image(img):

    img = img.convert("L")

    img = img.resize((OLED_WIDTH, OLED_HEIGHT), Image.NEAREST)

    img = img.convert("1", dither=Image.FLOYDSTEINBERG)
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
        ser.write(data)

        elapsed = time.perf_counter() - start
        time.sleep(max(0, frame_time - elapsed))

except KeyboardInterrupt:
    ser.close()
    print("Stopped streaming")
