import RPi.GPIO as gpio
import json
from mfrc522 import SimpleMFRC522
import time

#QApass diplay module placeholder
class QApassDisplay:
    def clear(self):
        print("[Display] Clear")

    def write_line(self, line, text):
        print(f"[Display] Line {line}: {text}")

    def show(self):
        print("[Display] Show")

reader = SimpleMFRC522()
display = QApassDisplay()
attendance_log = set

try:
    print("Place your card near the reader")
    while True:
        id, data = reader.read()
        print(f"Card read: {id}")

    try:
        student = json.loads(data)
        name = student.get("Name", "Unkown")
        srn = student.get("SRN", "Not Found")

        if id not in attendance_log:
            status = "Present"
            attendance_log.add(id)
        else:
            status = "Already Marked"

    except json.JSONDecodeError:
        print("Invalid json on card")
        display.clear()
        display.write_line(0, "Invalid card data")
        display.show()

    time.sleep(3)
    print("Ready for next scan...\n")

finally:
    gpio.cleanup()