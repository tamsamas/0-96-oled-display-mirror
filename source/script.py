import serial
import time
from PIL import ImageGrab, Image
import numpy as np

SERIAL_PORT = "/dev/tty.SLAB_USBtoUART"
BAUD_RATE = 115200
FPS = 20
OLED_WIDTH = 128
OLED_HEIGHT = 64

CROP_BOX = (0, 50, 480, 240)

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

def preprocess_image(img):
    # Convert to grayscale
    img = img.convert("L")
    
    # Resize with smoothing
    img = img.resize((OLED_WIDTH, OLED_HEIGHT), Image.LANCZOS)
    
    # Convert to 1-bit monochrome with dithering
    img = img.convert("1", dither=Image.FLOYDSTEINBERG)
    
    return img

try:
    while True:
        # Capture screen
        img = ImageGrab.grab(bbox=CROP_BOX)
        img = preprocess_image(img)

        # Convert to bytes for ESP32
        arr = np.array(img, dtype=np.uint8)
        data = np.packbits(arr, axis=1).tobytes()

        ser.write(data)
        time.sleep(1 / FPS)

except KeyboardInterrupt:
    ser.close()
    print("Stopped streaming")
