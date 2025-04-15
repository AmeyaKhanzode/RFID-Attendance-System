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
    today = time.strftime("%Y-%m-%d")
    subject = subject.lower()

    cursor.execute(
        f"SELECT * FROM {subject} WHERE srn = ? AND timestamp = ?", (srn, today))
    already_marked = cursor.fetchone()

    if already_marked:
        print(f"Attendance already marked today for {srn}")
    else:
        cursor.execute(
            f"INSERT INTO {subject} (srn, attended, timestamp) VALUES (?, ?, ?)",
            (srn, 1, today)
        )
        print(f"Inserted new attendance record for {srn} on {today}")

    conn.commit()
    conn.close()


def write_to_lcd(text):
    lcd.clear()
    lcd.write_string(text)


def read():
    try:
        lcd.write_string("Place card...")
        id, data = reader.read()
        lcd.clear()
        data = data.strip()
        student_info = json.loads(data)
        srn = student_info["srn"]
        subject = student_info["subject"]
        today = time.strftime("%Y-%m-%d")
        print(time.tzname)
        print(today)

        entry = db_utils.get_details(srn, subject)
        print(entry)

        if entry and len(entry[0]) > 4:
            if entry[0][4] == today:
                lcd.clear()
                lcd.write_string("Already marked!")
                buzzer.beep_error()
                time.sleep(2)
                lcd.clear()
                print(f"{srn} already marked for {subject} today.")
                return
        else:
            buzzer.beep_success()
            lcd.write_string(f"{srn[8:]}\n{subject.upper()}")
            print("testing")
            time.sleep(2)
            lcd.clear()
            lcd.write_string("Updated by 1")
            time.sleep(2)
            lcd.clear()

        increment_attended(srn, subject)
        print("Student info:", student_info)

    except json.JSONDecodeError:
        print("Error: Could not decode JSON data from the card.")
        print("Received raw data:", data)
        buzzer.beep_error()
