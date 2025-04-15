import json
import sqlite3
import time
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import buzzer

reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', 0x27)
DB_NAME = "attendance.db"

attendance_log = set()


def get_attendance_info(srn, subject):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(f"""
        SELECT attended, max_classes FROM {subject}
        WHERE srn = ?
    """, (srn,))
    result = cur.fetchone()
    conn.close()

    if result:
        attended, max_classes = result
        min_required = int(0.75 * max_classes)
        remaining_needed = max(0, min_required - attended)
        return attended, max_classes, remaining_needed
    else:
        return None, None, None


def mark_attendance(srn, subject, current_date):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(f"""
        UPDATE {subject}
        SET attended = attended + 1, last_marked_date = ?
        WHERE srn = ?
    """, (current_date, srn))
    conn.commit()
    conn.close()


def check_attendance():
    try:
        while True:
            lcd.clear()
            lcd.write_string("Tap your card...")

            id, data = reader.read()

            try:
                student = json.loads(data)
                buzzer.beep_success()
                srn = student["srn"]

                subjects = ["mpca", "cn"]
                found = False

                for subject in subjects:
                    attended, max_classes, remaining_needed = get_attendance_info(
                        srn, subject)

                    if attended is not None:
                        found = True

                        lcd.clear()
                        lcd.write_string(f"{srn[8:]}\n")
                        lcd.write_string(f"{subject.upper()}")
                        time.sleep(2)

                        lcd.clear()
                        lcd.write_string(f"Current:{attended}/{max_classes}")
                        time.sleep(2)

                        lcd.clear()
                        if remaining_needed == 0:
                            lcd.write_string("Need: none")
                        else:
                            lcd.write_string(f"Need: {remaining_needed} more")
                        time.sleep(2)

                if not found:
                    lcd.clear()
                    lcd.write_string("SRN not found")
                    time.sleep(2)

            except json.JSONDecodeError:
                buzzer.beep_error()
                lcd.clear()
                lcd.write_string("Invalid card")
                time.sleep(2)

            lcd.clear()
            lcd.write_string("Remove card...")
            time.sleep(1)
            break

            while True:
                try:
                    card_check = reader.read_no_block()
                    if card_check is None:
                        break
                except:
                    pass
                time.sleep(0.5)

            time.sleep(0.5)

    finally:
        lcd.clear()
