import RPi.GPIO as gpio
import sqlite3
import json
from mfrc522 import SimpleMFRC522
import buzzer
import db_utils

DB_NAME = "attendance.db"

reader = SimpleMFRC522()

db_utils.init()

def increment_attended(srn, subject):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    subject = subject.lower()

    if subject == "mpca":
        cursor.execute("SELECT * FROM mpca WHERE srn = ? ORDER BY id DESC LIMIT 1", (srn,))
    elif subject == "cn":
        cursor.execute("SELECT * FROM cn WHERE srn = ? ORDER BY id DESC LIMIT 1", (srn,))

    last_entry = cursor.fetchone()
    if last_entry:
        row_id, _, attended, _ = last_entry
        new_attended = int(attended) + 1

        if subject == "mpca":
            cursor.execute("UPDATE mpca SET attended = ? WHERE id = ?", (new_attended, row_id))
        elif subject == "cn":
            cursor.execute("UPDATE cn SET attended = ? WHERE id = ?", (new_attended, row_id))

        print(f"Attendance incremented to {new_attended} for {srn}")
    else:
        if subject == "mpca":
            cursor.execute("INSERT INTO mpca (srn, attended) VALUES (?, ?)", (srn, 1))
        elif subject == "cn":
            cursor.execute("INSERT INTO cn (srn, attended) VALUES (?, ?)", (srn, 1))
        print(f"Inserted new attendance record for {srn} with attended = 1")

    conn.commit()
    conn.close()

try:
    print("Place card near the reader:")
    id, data = reader.read()
    data = data.strip()
    student_info = json.loads(data)
    print("Student info:", student_info)

    increment_attended(student_info["srn"], student_info["subject"])
    buzzer.beep_success()

except json.JSONDecodeError:
    print("Error: Could not decode JSON data from the card.")
    print("Received raw data:", data)
    buzzer.beep_error()

finally:
    gpio.cleanup()