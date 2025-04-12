import RPi.GPIO as gpio
import json
from mfrc522 import SimpleMFRC522
import buzzer

reader = SimpleMFRC522()

try:
    print("place card near the reader:")
    id, data = reader.read()
    data = data.strip()
    student_info = json.loads(data)
    print("student info:", student_info)
    buzzer.beep_success()
except json.JSONDecodeError:
    print("error: couldnt not decode json data from the card.")
    print("recieved raw data:", data)
    buzzer.beep_error()
finally:
    gpio.cleanup()
