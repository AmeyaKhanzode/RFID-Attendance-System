import RPi.GPIO as gpio
from mfrc522 import SimpleMFRC522
import json
import time

reader = SimpleMFRC522()

print("Place card near the reader to write student data")
reader.write("hello")

print("Data written succefully!")
