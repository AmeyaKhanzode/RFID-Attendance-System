import RPi.GPIO as gpio
import json
import sqlite3
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import time

reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', 0x27)
DB_NAME = "attendance.db"

attendance_log = set()

# Fetch attendance data for a given subject


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


try:
    while True:
        lcd.clear()
        lcd.write_string("Tap your card...")

        id, data = reader.read()

        try:
            student = json.loads(data)
            print(student)
            srn = student["srn"]

            if id in attendance_log:
                lcd.clear()
                lcd.write_string("Already marked")
                time.sleep(2)
                continue
            else:
                attendance_log.add(id)

            # List of subjects to check
            subjects = ["mpca", "cn"]
            found = False

            for subject in subjects:
                attended, max_classes, remaining_needed = get_attendance_info(
                    srn, subject)

                if attended is not None:
                    found = True

                    # Subject name
                    lcd.clear()
                    lcd.write_string(f"{subject.upper()}")
                    time.sleep(2)

                    # Attendance count
                    lcd.clear()
                    lcd.write_string(f"{attended}/{max_classes}")
                    time.sleep(2)

                    # Required classes for 75%
                    lcd.clear()
                    if remaining_needed == 0:
                        lcd.write_string("Need: none")
                    else:
                        lcd.write_string(f"Need: {remaining_needed}")
                    time.sleep(2)

            if not found:
                lcd.clear()
                lcd.write_string("SRN not found")
                time.sleep(2)

        except json.JSONDecodeError:
            lcd.clear()
            lcd.write_string("Invalid card")
            time.sleep(2)

        # Wait until card is removed
        lcd.clear()
        lcd.write_string("Remove card...")
        time.sleep(1)

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
    gpio.cleanup()
