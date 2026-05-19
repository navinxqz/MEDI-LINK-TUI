// ═══════════════════════════════════════════════════
// OLED MINIMUM TEST — Upload this alone
// No DFPlayer, no buzzer, no Python needed
// Just ESP32 + OLED
// Open Serial Monitor at 115200 to see diagnosis
// ═══════════════════════════════════════════════════

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// ── Try changing these if still not working ─────────
// Standard ESP32 DevKit V1:  SDA=21, SCL=22
// ESP32-S2 / S3:             SDA=8,  SCL=9
// Try alternative:           SDA=4,  SCL=15
#define SDA_PIN 21
#define SCL_PIN 22

Adafruit_SSD1306 display(128, 64, &Wire, -1);

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("=== OLED TEST STARTING ===");

  // ── Start I2C ─────────────────────────────────────
  Wire.begin(SDA_PIN, SCL_PIN);
  delay(200);
  Serial.print("I2C started on SDA=");
  Serial.print(SDA_PIN);
  Serial.print(" SCL=");
  Serial.println(SCL_PIN);

  // ── Scan I2C bus for any device ───────────────────
  Serial.println("Scanning I2C bus...");
  int found = 0;
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    byte err = Wire.endTransmission();
    if (err == 0) {
      Serial.print("  Device found at 0x");
      if (addr < 16) Serial.print("0");
      Serial.print(addr, HEX);
      if      (addr == 0x3C) Serial.println(" <-- OLED (use 0x3C)");
      else if (addr == 0x3D) Serial.println(" <-- OLED (use 0x3D)");
      else                   Serial.println(" <-- unknown device");
      found++;
    }
  }

  if (found == 0) {
    Serial.println();
    Serial.println("!!! NO DEVICES FOUND !!!");
    Serial.println("This means wiring is wrong.");
    Serial.println("Check:");
    Serial.println("  VCC -> 3.3V (NOT 5V)");
    Serial.println("  GND -> GND");
    Serial.println("  SDA -> GPIO 21");
    Serial.println("  SCL -> GPIO 22");
    Serial.println("Press RST and try again.");
    // Blink built-in LED rapidly to signal no I2C device
    pinMode(2, OUTPUT);
    while (true) {
      digitalWrite(2, HIGH); delay(100);
      digitalWrite(2, LOW);  delay(100);
    }
  }

  // ── Try to init display at found address ──────────
  bool ok = false;
  byte oledAddr = 0;

  if (!ok) {
    if (display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
      ok = true; oledAddr = 0x3C;
    }
  }
  if (!ok) {
    if (display.begin(SSD1306_SWITCHCAPVCC, 0x3D)) {
      ok = true; oledAddr = 0x3D;
    }
  }

  if (!ok) {
    Serial.println("!!! OLED begin() FAILED !!!");
    Serial.println("Device found on I2C but display init failed.");
    Serial.println("Library may be wrong. Check:");
    Serial.println("  Adafruit SSD1306 library installed?");
    Serial.println("  Adafruit GFX library installed?");
    while (true);
  }

  // ── SUCCESS — draw test pattern ───────────────────
  Serial.print("[SUCCESS] OLED working at address 0x");
  Serial.println(oledAddr, HEX);
  Serial.println("You should see text on the display now.");
  Serial.print("Use this address in your main code: 0x");
  Serial.println(oledAddr, HEX);

  // Test 1: White fill
  display.fillScreen(SSD1306_WHITE);
  display.display();
  delay(600);

  // Test 2: Show text
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);

  display.setTextSize(2);
  display.setCursor(0, 0);
  display.println("WORKING!");

  display.setTextSize(1);
  display.setCursor(0, 22);
  display.print("Address: 0x");
  display.println(oledAddr, HEX);

  display.setCursor(0, 34);
  display.println("Medi-Link TUI 2.0");

  display.setCursor(0, 46);
  display.println("OLED test passed!");

  display.display();
}

void loop() {
  // Blink built-in LED slowly = test passed
  // Rapid blink = test failed
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH); delay(1000);
  digitalWrite(2, LOW);  delay(1000);
}
