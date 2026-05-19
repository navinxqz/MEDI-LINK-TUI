// Medi-Link TUI 2.0 — ESP32 Firmware
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include "DFRobotDFPlayerMini.h"

#define BUZZER_PIN  12
#define LED_PIN     13

Adafruit_SSD1306 display(128, 64, &Wire, -1);
HardwareSerial dfSerial(2); // UART2
DFRobotDFPlayerMini player;

void showOLED(String l1, String l2="", String l3="") {
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setTextSize(1);
  display.setCursor(0,0);  display.println(l1);
  display.setCursor(0,22); display.println(l2);
  display.setCursor(0,44); display.println(l3);
  display.display();
}
void setup() {
  Serial.begin(115200);
  dfSerial.begin(9600, SERIAL_8N1, 16, 17);
  pinMode(BUZZER_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
  if (!player.begin(dfSerial)) {
    showOLED("DFPlayer", "ERROR", "Check SD card");
    // don't hang — continue anyway
} else {
    player.volume(25);
}
showOLED("Medi-Link", "TUI 2.0", "Ready...");
}

void loop() {
  if (Serial.available()) {
    String msg = Serial.readStringUntil('\n');
    if (msg.startsWith("WARN")) {
      showOLED("!! DANGER !!",
               msg.substring(5),
               "DO NOT take!");
      digitalWrite(LED_PIN, HIGH);
      digitalWrite(BUZZER_PIN, HIGH);
      delay(800);
      digitalWrite(BUZZER_PIN, LOW);
      player.play(2);
    } else if (msg.startsWith("EXPR")) {
      showOLED("EXPIRED MED",
             msg.substring(5),
               "Check package!");
      player.play(3);
    } else {
      showOLED("IDENTIFIED:", msg, "STATUS: SAFE");
      digitalWrite(LED_PIN, LOW);
      player.play(1);
    }
  }
}