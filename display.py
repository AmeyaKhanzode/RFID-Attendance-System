import RPi.GPIO as gpio
import json
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import time
import buzzer

reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', 0x27)

attendance_log = set()

try:
    while True:
        lcd.clear()
        lcd.write_string("Tap your card...")

        id, data = reader.read()

        try:
            student = json.loads(data.strip())
            srn = student.get("srn", "Unknown")
            subject = student.get("subject", "Unknown")

            if id in attendance_log:
                status = "Already Marked"
            else:
                attendance_log.add(id)
                status = "Marked Present"

            buzzer.beep_success()

            lcd.clear()
            lcd.write_string(f"SRN:\n{srn[:16]}")
            time.sleep(2)

            lcd.clear()
            lcd.write_string(f"Status:\n{status[:16]}")
            time.sleep(2)

        except json.JSONDecodeError:
            lcd.clear()
            lcd.write_string("Invalid card data")
            buzzer.beep_error()
            time.sleep(2)

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