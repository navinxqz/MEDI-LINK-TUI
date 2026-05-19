#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ── Pins ────────────────────────────────────────────
#define OLED_SDA   21
#define OLED_SCL   22

// ── OLED object configuration (128x64 display) ──────
Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
  Serial.begin(115200);
  delay(500);

  // Initialize I2C communication
  Wire.begin(OLED_SDA, OLED_SCL);
  delay(100);

  // Initialize the OLED screen (try standard 0x3C first)
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("[ERROR] SSD1306 allocation failed. Checking 0x3D..."));
    if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3D)) {
      Serial.println(F("[ERROR] OLED screen not detected. Halting."));
      while(true); // Loop forever if screen is missing
    }
  }

  Serial.println(F("[OK] OLED Initialized successfully!"));

  // Clear the internal buffer
  display.clearDisplay();

  // Draw a standard testing sequence
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  
  display.setCursor(0, 0);
  display.println("=== SYSTEM READY ===");
  
  display.setCursor(0, 20);
  display.println("I2C Pins: SDA=21, SCL=22");
  
  display.setCursor(0, 40);
  display.println("Status: Operational");
  
  // Push the buffer data to the physical screen hardware
  display.display();
}

void loop() {
  // Static visual test. Loop intentionally left blank.
}
