import RPi.GPIO as gpio
import sqlite3
import time
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import buzzer

DB_NAME = "attendance.db"
MASTER_ID = 123456789  # Replace with master card ID

reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', 0x27)

def show_message(message, delay=2):
    lcd.clear()
    lines = message.split("\n")
    for i, line in enumerate(lines):
        lcd.cursor_pos = (i, 0)
        lcd.write_string(line[:16])
    time.sleep(delay)

def delete():
    try:
        show_message("Scan Card")
        id, _ = reader.read()

        if id != MASTER_ID:
            show_message("Unauthorized\nAccess")
            buzzer.beep_error()
            return

        srn = input("Enter SRN to delete attendance from: ").strip()
        subject = input("Enter subject (MPCA / CN): ").strip().lower()

        if subject not in ["mpca", "cn"]:
            show_message("Invalid Subject")
            buzzer.beep_error()
            return

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute(f"SELECT attended, max_classes FROM {subject} WHERE srn = ?", (srn,))
        result = cursor.fetchone()

        if result:
            attended, max_classes = result
            if attended > 0:
                cursor.execute(f"UPDATE {subject} SET attended = ? WHERE srn = ?", (attended - 1, srn))
                conn.commit()
                show_message("Decreased by 1", delay=2)
                show_message(f"{srn}: {attended - 1}/{max_classes}")
                buzzer.beep_success()
            else:
                show_message("Attendance\nis zero")
                buzzer.beep_error()
        else:
            show_message("SRN not found")
            buzzer.beep_error()

        conn.close()

    finally:
        lcd.clear()
        gpio.cleanup()