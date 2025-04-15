from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import json
import buzzer

reader = SimpleMFRC522()

lcd = CharLCD('PCF8574', 0x27)


def create_student_details():
    srn = input("Enter SRN: ")
    subject = input("Subject: ")
    return {
        "srn": srn,
        "subject": subject
    }


def write():
    try:
        data = create_student_details()
        data_serialised = json.dumps(data)

        print("Data to be written to card:", data_serialised)
        lcd.clear()
        lcd.write_string("Place Card...")

        reader.write(data_serialised)

        buzzer.beep_success()
        lcd.clear()
        lcd.write_string("Data Written!")

    except Exception as e:
        print(f"Error while writing to card: {e}")
