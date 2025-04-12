import RPi.GPIO as GPIO
import time

BUZZER_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(BUZZER_PIN, GPIO.HIGH)

def beep_success():
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def beep_error():
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(0.6)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)

def cleanup_buzzer():
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        beep_success()
        time.sleep(1)
        beep_error()
    finally:
        cleanup_buzzer()