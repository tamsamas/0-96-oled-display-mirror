#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire);

void setup() {
  Serial.begin(115200);
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    for(;;);
  }
  display.clearDisplay();
  display.display();
}

void loop() {
  static uint8_t buffer[1024];  
  static int index = 0;

  while (Serial.available()) {
    buffer[index++] = Serial.read();
    if (index >= 1024) {
      index = 0;

      display.clearDisplay();
      display.drawBitmap(0, 0, buffer, 128, 64, SSD1306_WHITE);
      display.display();
    }
  }
}
