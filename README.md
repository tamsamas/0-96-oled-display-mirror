I made this out of boredom and feel free to make changes to the code. I also used an ESP32 to do this, with the OLED display connected to it. (i personally used pin 22 on the ESP32 for the SCL pin on the oled, and pin 21 for SDA.) Run the python script on your computer and flash the ino file to your microcontroller.
Make sure to be connected via USB

Also, you can set a custom place on your display that you want to specifically mirror to your oled.

Side note: use 230400–460800 baud rate for more stable video transmission - Make sure to match for the both codes.
If the image is glitched out, try 115200. If you're on linux, you're gonna have some issues at first. Try the code made specifically for linux machines.

BTW THE CODE SHOULD WORK OUT OF THE BOX!! Just flash and run the py script. If it doesn't work, here's how to fix:
List the USBtoUART chips and find your ESP32 or any microcontroller that works with my code, and copy the output and replace it in the python script.
Example:

WINDOWS: SERIAL_PORT = "COM5"

LINUX: SERIAL_PORT = "/dev/ttyUSB0"

MACOS: SERIAL_PORT = "/dev/tty.SLAB_USBtoUART"

Btw if ur on windows, try linux or the macos code and see which works the best for you. This code was tested and made on macOS.
