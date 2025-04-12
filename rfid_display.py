import RPi.GPIO as gpio
import json
from mfrc522 import SimpleMFRC522
import time

reader = SimpleMFRC522()
attendance_log = set()

try:
    while True:
        print("Place your card near the reader:")
        id, data = reader.read()
        print(f"Card read: {id}")

        try:
            student = json.loads(data)
            name = student.get("Name", "Unknown")
            srn = student.get("SRN", "Not Found")

            if id not in attendance_log:
                status = "Present"
                attendance_log.add(id)
            else:
                status = "Already Marked"

            print(f"Name: {name}, SRN: {srn}, Status: {status}")

        except json.JSONDecodeError:
            print("Invalid data on card.")

        print("Remove card to continue...")
        time.sleep(1)

        while True:
            try:
                reader.read_no_block()
            except:
                pass
            time.sleep(0.5)
            if reader.read_no_block() is None:
                break

        time.sleep(0.5)

finally:
    gpio.cleanup()