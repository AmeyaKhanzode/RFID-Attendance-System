import RPi.GPIO as gpio
from mfrc522 import SimpleMFRC522
import json
import time

reader = SimpleMFRC522()

def create_student_details():
    srn = input("Enter SRN: ")
    subject = input("Subject: ")

    return {
        "srn":srn,
        "subject":subject
    }


data = create_student_details()

data_serialised = json.dumps(data)
print("Data to be written to card:", data_serialised)
print("Place card near the reader to write student data")
reader.write(data_serialised)

print("Data written succefully!")