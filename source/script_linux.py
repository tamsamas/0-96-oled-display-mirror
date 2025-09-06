import sys
import time
import serial
import serial.tools.list_ports
import numpy as np
from PIL import Image

# ==== Multiplatform screen capture ====
if sys.platform.startswith("linux"):
    import mss

    def grab_screen(bbox=None):
        with mss.mss() as sct:
            monitor = sct.monitors[0] if bbox is None else {"top": bbox[1], "left": bbox[0], "width": bbox[2]-bbox[0], "height": bbox[3]-bbox[1]}
            img = sct.grab(monitor)
            img = Image.frombytes("RGB", img.size, img.rgb)
            return img
else:
    from PIL import ImageGrab

    def grab_screen(bbox=None):
        return ImageGrab.grab(bbox=bbox)

# ==== CONFIG ====
for port in serial.tools.list_ports.comports():
    print(port)
print("Choose the serial port for your ESP32")
SERIAL_PORT = input("Port : ")
BAUD_RATE = 460800
FPS = 30
OLED_WIDTH = 128
OLED_HEIGHT = 64
CROP_BOX = None  # (left, top, right, bottom) or None = full screen

# ==== SERIAL SETUP ====
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)

# ==== IMAGE PROCESSING ====
def preprocess_image(img):
    img = img.convert("L")  # grayscale
    img = img.resize((OLED_WIDTH, OLED_HEIGHT), Image.NEAREST)
    img = img.point(lambda x: 0 if x < 128 else 1, '1')  # 1-bit threshold
    return img

def image_to_rowmajor(img):
    arr = np.array(img, dtype=np.uint8)  # 0/1
    data = bytearray()
    for y in range(OLED_HEIGHT):
        row = arr[y, :]
        packed = np.packbits(row, axis=0)
        data.extend(packed)
    return bytes(data)  # 1024 bytes

# ==== MAIN LOOP ====
frame_time = 1 / FPS

try:
    while True:
        start = time.perf_counter()

        img = grab_screen(bbox=CROP_BOX)
        img = preprocess_image(img)
        data = image_to_rowmajor(img)

        # send sync marker + frame
        ser.write(b"\xAA")
        ser.write(data)

        elapsed = time.perf_counter() - start
        time.sleep(max(0, frame_time - elapsed))

except KeyboardInterrupt:
    ser.close()
    print("Stopped streaming")
