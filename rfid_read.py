import RPi.GPIO as gpio
import sqlite3
import json
from mfrc522 import SimpleMFRC522
import buzzer
import db_utils

DB_NAME = "attendance.db"

reader = SimpleMFRC522()

db_utils.init()


def increment_attended(srn):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM mpca WHERE SRN = ? ORDER BY id DESC LIMIT 1", (srn,))

    last_entry = cursor.fetchone()
    if last_entry:
        row_id, attended = last_entry[0], last_entry[2]
        new_attended = int(attended) + 1
        cursor.execute("""
            UPDATE mpca SET attended = ? WHERE id = ?
        """, (new_attended, row_id))
        conn.commit()
        print(f"Attendance incremented to {new_attended} for {srn}")
    else:
        print(f"No entry found for SRN {srn}, inserting new one.")
    print(last_entry)


try:
    print("place card near the reader:")
    id, data = reader.read()
    data = data.strip()
    student_info = json.loads(data)
    print("student info:", student_info)
    buzzer.beep_success()
    increment_attended(student_info["srn"])
    # db_utils.insert_attendance(student_info)
except json.JSONDecodeError:
    print("error: couldnt not decode json data from the card.")
    print("recieved raw data:", data)
    buzzer.beep_error()
finally:
    gpio.cleanup()
