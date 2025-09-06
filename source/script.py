import serial
import time
from PIL import ImageGrab, Image
import numpy as np

SERIAL_PORT = "/dev/tty.SLAB_USBtoUART"
BAUD_RATE = 115200
FPS = 20
OLED_WIDTH = 128
OLED_HEIGHT = 64

CROP_BOX = None

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2)

def preprocess_image(img):
    img = img.convert("L")
    
    img = img.resize((OLED_WIDTH, OLED_HEIGHT), Image.LANCZOS)
    
    img = img.convert("1", dither=Image.FLOYDSTEINBERG)
    
    return img

try:
    while True:
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
