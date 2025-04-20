from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()


id, data = reader.read()

print(id)
