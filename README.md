I made this out of boredom and feel free to make changes to the code. I also used an ESP32 to do this, with the OLED display connected to it. (i personally used pin 22 on the ESP32 for the SCL pin on the oled, and pin 21 for SDA.) Run the python script on your computer and flash the ino file to your microcontroller.
Make sure to be connected via USB

Also, you can set a custom place on your display that you want to specifically mirror to your oled.

Side note: use 230400–460800 baud rate for more stable video transmission - Make sure to match for the both codes.
If the image is glitched out, try 115200. If you're on linux, you're gonna have some issues at first. Try the code made specifically for linux machines. If you're on windows tho, you're out of luck.

BTW THE CODE SHOULD WORK OUT OF THE BOX!! (on macOS at least) Just flash and run the py script.

This code was tested and made on macOS.
