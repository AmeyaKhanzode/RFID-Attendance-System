import RPi.GPIO as gpio
from mfrc522 import SimpleMFRC522
import json
import buzzer

reader = SimpleMFRC522()

def create_student_details():
    srn = input("Enter SRN: ").strip()
    subject = input("Subject (MPCA or CN): ").strip().lower()
    return {
        "srn": srn,
        "subject": subject
    }

data = create_student_details()

data_serialised = json.dumps(data)
print("Data to be written to card:", data_serialised)
print("Place card near the reader to write student data")

try:
    reader.write(data_serialised)
    buzzer.beep_success()
    print("Data written successfully!")
finally:
    gpio.cleanup()