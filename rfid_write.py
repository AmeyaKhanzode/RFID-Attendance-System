import RPi.GPIO as gpio
from mfrc522 import SimpleMFRC522
import json

reader = SimpleMFRC522()

try:
    data = {"Name":"Ameya", "Age":20}
    text = json.dumps(data)
    print("Place card near the reader to write")
    reader.write(text)
    print("Data written on card succesfully!")
finally:
    gpio.cleanup()
