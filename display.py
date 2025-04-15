import RPi.GPIO as gpio
import json
import sqlite3
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import time
from datetime import datetime

reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', 0x27)
DB_NAME = "attendance.db"

# Fetch attendance data for a given subject
def get_attendance_info(srn, subject):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute(f"""
        SELECT attended, max_classes, last_marked_date FROM {subject}
        WHERE srn = ?
    """, (srn,))
    result = cur.fetchone()
    conn.close()

    if result:
        attended, max_classes, last_marked_date = result
        min_required = int(0.75 * max_classes)
        remaining_needed = max(0, min_required - attended)
        return attended, max_classes, remaining_needed, last_marked_date
    else:
        return None, None, None, None

# Update attendance if not already marked today
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

try:
    while True:
        lcd.clear()
        lcd.write_string("Tap your card...")

        id, data = reader.read()

        try:
            student = json.loads(data)
            print(student)
            srn = student["srn"]

            # List of subjects to check
            subjects = ["mpca", "cn"]
            found = False
            current_date = datetime.now().strftime("%Y-%m-%d")

            for subject in subjects:
                attended, max_classes, remaining_needed, last_marked_date = get_attendance_info(srn, subject)

                if attended is not None:
                    found = True

                    if last_marked_date == current_date:
                        lcd.clear()
                        lcd.write_string("Already marked")
                        lcd.crlf()
                        lcd.write_string(subject.upper())
                        time.sleep(2)
                        continue

                    # Mark attendance
                    mark_attendance(srn, subject, current_date)

                    # Update values after marking
                    attended += 1
                    remaining_needed = max(0, int(0.75 * max_classes) - attended)

                    # Display updated info
                    lcd.clear()
                    lcd.write_string(f"{subject.upper()}: {attended}/{max_classes}")
                    lcd.crlf()
                    lcd.write_string(f"NEEDED: {remaining_needed}")
                    time.sleep(3)

            if not found:
                lcd.clear()
                lcd.write_string("SRN not found")
                lcd.crlf()
                lcd.write_string("Remove card...")
                time.sleep(2)

        except json.JSONDecodeError:
            lcd.clear()
            lcd.write_string("Invalid card")
            lcd.crlf()
            lcd.write_string("Remove card...")
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
