import RPi.GPIO as gpio
import json
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import time

reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', 0x27)  # Adjust address if needed

# To keep track of already marked students (optional)
attendance_log = set()

try:
    while True:
        lcd.clear()
        lcd.write_string("Tap your card...")

        # Wait for card and read data
        id, data = reader.read()

        try:
            student = json.loads(data)
            srn = student.get("SRN", "Not Found")
            status = student.get("attendance", "Unknown")

            # Prevent duplicates
            if id in attendance_log:
                status = "Already Marked"
            else:
                attendance_log.add(id)

            # Display SRN
            lcd.clear()
            lcd.write_string(f"SRN:\n{srn[:16]}")
            time.sleep(2)

            # Display Status
            lcd.clear()
            lcd.write_string(f"Status:\n{status[:16]}")
            time.sleep(2)

        except json.JSONDecodeError:
            lcd.clear()
            lcd.write_string("Invalid card data")
            time.sleep(2)

        # Wait for card to be removed
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

        # Buffer delay after removal
        time.sleep(0.5)

finally:
    lcd.clear()
    gpio.cleanup()
