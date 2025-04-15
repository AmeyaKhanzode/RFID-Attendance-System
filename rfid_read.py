import time
import sqlite3
import json
from mfrc522 import SimpleMFRC522
import buzzer
from RPLCD.i2c import CharLCD
import db_utils

DB_NAME = "attendance.db"

reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', 0x27)

db_utils.init()


def increment_attended(srn, subject):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    subject = subject.lower()

    cursor.execute(
        f"SELECT * FROM {subject} WHERE srn = ? ORDER BY id DESC LIMIT 1", (srn,))
    last_entry = cursor.fetchone()
    if last_entry:
        row_id, _, attended, _ = last_entry
        new_attended = int(attended) + 1
        cursor.execute(
            f"UPDATE {subject} SET attended = ? WHERE id = ?", (new_attended, row_id))
        print(f"Attendance incremented to {new_attended} for {srn}")
    else:
        cursor.execute(
            f"INSERT INTO {subject} (srn, attended) VALUES (?, ?)", (srn, 1))
        print(f"Inserted new attendance record for {srn} with attended = 1")

    conn.commit()
    conn.close()


def write_to_lcd(text):
    lcd.clear()
    lcd.write_string(text)


def read():
    try:
        write_to_lcd("Place card...")
        id, data = reader.read()
        swiped = 1
        data = data.strip()
        student_info = json.loads(data)
        srn = student_info["srn"]
        subject = student_info["subject"]
        buzzer.beep_success()
        lcd.clear()
        lcd.write_string(f"{srn[8:]}\n")
        lcd.write_string(f"{subject.upper()}")
        time.sleep(2)
        lcd.clear()
        lcd.write_string("Updated by 1")
        print("Student info:", student_info)

        increment_attended(srn, subject)

    except json.JSONDecodeError:
        print("Error: Could not decode JSON data from the card.")
        print("Received raw data:", data)
        buzzer.beep_error()
