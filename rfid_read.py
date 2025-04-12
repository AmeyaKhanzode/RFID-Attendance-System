import RPi.GPIO as gpio
import json
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    print("Place card near the reader:")
    id, data = reader.read()
    text = json.loads(data)
    print(f"ID: {id} | Text: {text}")
finally:
    gpio.cleanup()
