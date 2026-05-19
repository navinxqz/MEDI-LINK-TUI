import cv2
import cv2.aruco as aruco
import serial
import pandas as pd
from datetime import datetime
import time
import requests

# ── TELEGRAM CONFIG ────────────────────────────
TG_TOKEN = '8613841212:AAHZm7njBR6a49Fk9zsxOHhsUlFOhhUc-PQ'
TG_CHAT_ID = '5057900072'


def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"

        data = {
            "chat_id": TG_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }

        requests.post(url, data=data, timeout=5)

        print(f"[TG] Sent: {message}")

    except Exception as e:
        print(f"[TG] Failed: {e}")


# ── CONFIG ─────────────────────────────────────
PORT = 'COM3'     # change to your port
BAUD = 115200
CAM_IDX = 0

# ── MEDICINE DATABASE ──────────────────────────
# {ID: (Name, Expiry YYYY-MM)}
med_db = {
    0: ("Napa", "2027-06"),
    1: ("Seclo", "2026-03"),
    2: ("Clopidogrel", "2025-11"),
    3: ("Warfarin", "2026-08"),
    4: ("Aspirin", "2027-01"),
    5: ("Metformin", "2026-12"),
}

# ── DANGER PAIRS ───────────────────────────────
danger_pairs = {
    frozenset([1, 2]): "Seclo+Clopidogrel",
    frozenset([2, 3]): "Clopi+Warfarin",
    frozenset([3, 4]): "Warfarin+Aspirin",
    frozenset([0, 2]): "Napa+Clopidogrel",
    frozenset([4, 5]): "Aspirin+Metformin",
}

# ── LOGGING ────────────────────────────────────
def log_event(ids, status, desc):

    entry = {
        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "IDs": str(list(ids)),
        "Meds": ", ".join([med_db[i][0] for i in ids if i in med_db]),
        "Status": status,
        "Detail": desc
    }

    pd.DataFrame([entry]).to_csv(
        "patient_log.csv",
        mode='a',
        header=False,
        index=False
    )


# ── EXPIRY CHECK ───────────────────────────────
def check_expiry(med_id):

    now = datetime.now().strftime("%Y-%m")
    exp = med_db[med_id][1]

    return exp < now


# ── SERIAL CONNECT ─────────────────────────────
try:
    ser = serial.Serial(PORT, BAUD, timeout=1)

    time.sleep(2)

    print(f"[OK] Connected: {PORT}")

except:
    print("[ERROR] Serial failed. Check PORT value.")

    ser = None


# ── ARUCO SETUP ────────────────────────────────
cap = cv2.VideoCapture(CAM_IDX)

adict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

params = aruco.DetectorParameters()

det = aruco.ArucoDetector(adict, params)

print("[START] Medi-Link running. Press Q to quit.")

last_sig = None


# ── MAIN LOOP ──────────────────────────────────
while True:

    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, _ = det.detectMarkers(gray)

    if ids is not None:

        aruco.drawDetectedMarkers(frame, corners, ids)

        detected = set(ids.flatten().tolist())

        # ── CHECK EXPIRY ────────────────────────
        expired = [
            i for i in detected
            if i in med_db and check_expiry(i)
        ]

        if expired:

            name = med_db[expired[0]][0]

            msg = f"EXPR:{name}"

            if ser:
                ser.write((msg + '\n').encode())

            log_event(detected, "EXPIRED", name)

            if msg != last_sig:

                send_telegram(
                    f"⏰ <b>EXPIRED MEDICINE</b>\n"
                    f"💊 Medicine: <b>{name}</b>\n"
                    f"📋 Please replace this medicine!"
                )

                last_sig = msg

            cv2.putText(
                frame,
                f"EXPIRED: {name}",
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

        else:

            # ── CHECK DANGER INTERACTION ───────
            danger = None

            for pair, desc in danger_pairs.items():

                if pair.issubset(detected):

                    danger = desc
                    break

            names = ", ".join([
                med_db[i][0]
                for i in detected
                if i in med_db
            ])

            # ── DANGER FOUND ───────────────────
            if danger:

                msg = f"WARN:{danger}"

                color = (0, 0, 255)

                if msg != last_sig:

                    if ser:
                        ser.write((msg + '\n').encode())

                    log_event(detected, "DANGER", danger)

                    patient_meds = ", ".join([
                        med_db[i][0]
                        for i in detected
                        if i in med_db
                    ])

                    alert = (
                        f"⚠️ <b>DANGER: Drug Interaction</b>\n"
                        f"💊 Medicines: <b>{patient_meds}</b>\n"
                        f"❌ Interaction: {danger}\n"
                        f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}\n"
                        f"📋 Action: Do NOT take these together!"
                    )

                    send_telegram(alert)

                    last_sig = msg

            # ── SAFE ───────────────────────────
            else:

                msg = names

                color = (0, 255, 0)

                if msg != last_sig:

                    if ser:
                        ser.write((msg + '\n').encode())

                    log_event(detected, "SAFE", names)

                    last_sig = msg

            # ── DISPLAY TEXT ───────────────────
            cv2.putText(
                frame,
                msg[:50],
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

    else:

        cv2.putText(
            frame,
            "No blocks detected",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (150, 150, 150),
            1
        )

        last_sig = None

    # ── SHOW WINDOW ────────────────────────────
    cv2.imshow("Medi-Link TUI 2.0", frame)

    # ── PRESS Q TO EXIT ───────────────────────
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ── CLEANUP ────────────────────────────────────
cap.release()

cv2.destroyAllWindows()

if ser:
    ser.close()

print("[DONE] Check patient_log.csv")