# 🩺 MEDI-LINK TUI 2.0
### *An IoT-Enabled Tangible User Interface for Geriatric Medication Safety*

<p align="center">
  <img src="https://raw.githubusercontent.com/navinxqz/MEDI-LINK-TUI/main/ArUco/circuit.jpeg" alt="MEDI-LINK TUI Circuit" width="850"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AIUB-CSE-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python-3.11-yellow?style=for-the-badge&logo=python"/>
  <img src="https://img.shields.io/badge/ESP32-IoT-red?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/OpenCV-ArUco-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Flask-Dashboard-black?style=for-the-badge"/>
</p>

---

# 📌 Project Overview

**MEDI-LINK TUI 2.0** is a real-time smart medication safety system designed for elderly patients.  
The system uses a **Tangible User Interface (TUI)** where users interact with physical medicine blocks instead of mobile apps or touchscreens.

A webcam detects ArUco markers attached to medicine blocks using **OpenCV**, then checks for:

- Dangerous drug-drug interactions (DDI)
- Expired medicines
- Safe medication combinations

If a dangerous combination is detected:

- 🚨 OLED warning is displayed
- 🔊 Buzzer alert is triggered
- 📲 Telegram notification is sent to caregivers
- 📊 Event is logged into a live Flask dashboard

---

# ✨ Key Features

<details open>
<summary><strong>🧠 Core Functionalities</strong></summary>

- Tangible User Interface (TUI) for elderly accessibility
- Real-time ArUco marker detection
- Drug-Drug Interaction (DDI) checking
- Medicine expiry verification
- OLED warning display
- Multi-pattern buzzer alert system
- Telegram caregiver notification
- Flask live monitoring dashboard
- CSV-based patient event logging
- Offline-first architecture

</details>

<details open>
<summary><strong>🧑‍⚕️ Accessibility & HCI Principles</strong></summary>

- Zero typing or touchscreen interaction
- Large visual feedback via OLED
- Audio feedback through buzzer patterns
- Error prevention using physical medicine blocks
- Designed for low digital literacy elderly users

</details>

---

# 🏗️ System Architecture

```text
Medicine Blocks (ArUco)
            │
            ▼
      Webcam Detection
            │
            ▼
      Python + OpenCV
            │
 ┌──────────┼──────────┐
 ▼          ▼          ▼
DDI Check  Expiry     Logging
            │
            ▼
      Serial Communication
            │
            ▼
            ESP32
     ┌───────────────┐
     ▼               ▼
 OLED Display     Buzzer Alert
     │
     ▼
 Telegram Notification
     │
     ▼
 Flask Dashboard
```

---

# 🧰 Tech Stack

| Category | Technologies |
|---|---|
| Programming Language | Python, C++ |
| Computer Vision | OpenCV, ArUco |
| Hardware | ESP32 DevKit V1 |
| Dashboard | Flask |
| Communication | PySerial |
| Notifications | Telegram Bot API |
| Data Logging | Pandas CSV |
| UI | OLED SSD1306 |
| IDE | Arduino IDE |

---

# 🔌 Hardware Components

<details open>
<summary><strong>📦 Hardware List</strong></summary>

| Component | Purpose |
|---|---|
| ESP32 DevKit V1 | Main microcontroller |
| OLED SSD1306 (0.96") | Display alerts/status |
| Active Buzzer | Audio feedback |
| Webcam | ArUco detection |
| LEDs | Lighting and indicators |
| Breadboard + Jumper Wires | Circuit connections |
| Medicine Blocks | Tangible medicine representation |

</details>

---

# 🔧 Circuit Connection

| Component Pin | ESP32 Pin |
|---|---|
| OLED SDA | GPIO 21 |
| OLED SCL | GPIO 22 |
| Buzzer + | GPIO 12 |
| LED + | GPIO 13 |
| OLED VCC | 3.3V |
| OLED GND | GND |

> ⚠️ Always connect OLED VCC to **3.3V**, never 5V.

---

# 📁 Project Structure

```bash
MEDI-LINK-TUI/
│
├── ArUco/
│   ├── circuit.jpeg
│   ├── markers/
│
├── medilink.py
├── dashboard.py
├── patient_log.csv
│
├── firmware/
│   ├── medilink_firmware.ino
│
├── README.md
│
└── requirements.txt
```

---

# ⚙️ Installation Guide

<details open>
<summary><strong>🐍 Python Environment Setup</strong></summary>

## 1️⃣ Install Python

Download Python 3.11 from:

https://www.python.org/downloads/

---

## 2️⃣ Install Required Libraries

```bash
pip install opencv-python
pip install opencv-contrib-python
pip install pyserial
pip install pandas
pip install requests
pip install flask
```

</details>

---

# 🔥 ESP32 Setup

<details open>
<summary><strong>📡 Arduino IDE Setup</strong></summary>

## Install ESP32 Board Package

Add this URL in:

```text
Arduino IDE → Preferences → Additional Boards Manager URLs
```

```text
https://dl.espressif.com/dl/package_esp32_index.json
```

Then install:

```text
ESP32 by Espressif Systems
```

---

## Required Arduino Libraries

Install from Library Manager:

- Adafruit SSD1306
- Adafruit GFX Library
- DFRobotDFPlayerMini (optional)

</details>

---

# 🚀 Running the Project

## Step 1 — Upload ESP32 Firmware

Upload the firmware using Arduino IDE.

---

## Step 2 — Run Main Detection Script

```bash
python medilink.py
```

---

## Step 3 — Run Dashboard

Open another terminal:

```bash
python dashboard.py
```

Open browser:

```text
http://localhost:5000
```

---

# 📲 Telegram Bot Integration

<details>
<summary><strong>📨 Telegram Alert Setup</strong></summary>

1. Open Telegram
2. Search `@BotFather`
3. Create a bot using `/newbot`
4. Copy Bot Token
5. Get Chat ID from:

```text
https://api.telegram.org/botYOUR_TOKEN/getUpdates
```

6. Add credentials inside:

```python
TG_TOKEN = 'YOUR_BOT_TOKEN'
TG_CHAT_ID = 'YOUR_CHAT_ID'
```

</details>

---

# 📊 Dashboard Features

- Live medication event monitoring
- Safe vs danger event charts
- Medicine usage analytics
- Recent activity table
- Auto-refresh every 5 seconds
- Accessible from mobile devices on same WiFi

---

# 🧪 Sample Detection Flow

| Scenario | System Response |
|---|---|
| Safe Medicine | Green status + short beep |
| Dangerous Combination | Red warning + 3 long beeps |
| Expired Medicine | Expiry warning + 2 medium beeps |

---

# 🖥️ Example Dangerous Pair Database

```python
danger_pairs = {
    frozenset([1, 2]): 'Seclo+Clopidogrel',
    frozenset([2, 3]): 'Clopi+Warfarin',
    frozenset([3, 4]): 'Warfarin+Aspirin',
}
```

---

# 📸 Project Preview

<p align="center">
  <img src="https://raw.githubusercontent.com/navinxqz/MEDI-LINK-TUI/main/ArUco/circuit.jpeg" width="850"/>
</p>

---

# 🧠 Research & Academic Value

This project demonstrates concepts from:

- Human Computer Interaction (HCI)
- Tangible User Interfaces (TUI)
- Internet of Things (IoT)
- Embedded Systems
- Computer Vision
- Healthcare Informatics
- Assistive Technology

---

# 📚 Future Improvements

- Cloud database integration
- AI-based prescription analysis
- Voice assistant integration
- Mobile app companion
- QR code medicine database
- Edge AI detection on ESP32-CAM

---

# 🛡️ License

This project is intended for:

- Academic Research
- Educational Demonstration
- Non-commercial Use

---

<!-- # ⭐ Acknowledgements

Special thanks to:

- OpenCV Community
- Espressif Systems
- Arduino Community
- Flask Developers
- Telegram Bot API

--- -->

# 📬 Contact

For collaboration, research, or academic discussion: navinmdnawshin@gmail.com

<h2 align="left">Contributors</h2>

####
<table>
   <div style = "display: flex; align-item: flex-start; align: center">
      <table align= "center">
         <tr>
            <td align = "center" width = "200"><img src= "https://avatars.githubusercontent.com/u/170220890?v=4" width="auto" height= "auto"/></td>
            <td align = "center" width = "200"><img src= "https://avatars.githubusercontent.com/u/169520102?v=4" width="auto" height= "auto"/></td>
            <td align = "center" width = "200"><img src= "https://media.licdn.com/dms/image/v2/D5603AQH1yCMfCqi2dw/profile-displayphoto-shrink_400_400/B56ZWlBcjiHQAg-/0/1742230378599?e=1781136000&v=beta&t=HofePh82qZFlZ2b2LOeqsiiLjveObgJKJelqphdb0ng" width="auto" height= "auto"/></td>
            <td align = "center" width = "200"><img src= "https://media.licdn.com/dms/image/v2/D5603AQEUpp-1kG9j1w/profile-displayphoto-shrink_400_400/B56Zbyc4fCHgAs-/0/1747824380904?e=1781136000&v=beta&t=ywP3SSZ74cu_qzsoE3XYnVQHwnYKitC4JTABKj1R8OQ" width="auto" height= "auto"/></td>
         </tr><tr>
            <td align = "center" width = "200"><a href="https://github.com/SADMANTANZIM" target="_blank">Sadman Shabab</td>
            <td align = "center" width = "200"><a href="https://github.com/navinxqz" target="_blank">Navin, Md Nawshin</td>
            <td align = "center" width = "200"><a href="https://www.linkedin.com/in/sudipto9261/" target="_blank" alt="Sudipto LinkedIn">Sudipto Mondal</td>
            <td align = "center" width = "200"><a href="https://www.linkedin.com/in/sanjida-islam-disha-21229b280/" alt="Disha LinkedIn" target="_blank">Sanjida Disha</td>
         </tr></table>
    </div>
</table>
