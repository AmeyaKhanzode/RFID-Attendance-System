import RPi.GPIO as GPIO
import time

BUZZER_PIN = 11  # Using GPIO.BOARD pin 11 (change to 17 if using BCM mode)


def setup_buzzer():
    GPIO.setup(BUZZER_PIN, GPIO.OUT)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)


def beep_success():
    for _ in range(3):
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(0.07)
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(0.07)


def beep_error():
    GPIO.output(BUZZER_PIN, GPIO.LOW)
    time.sleep(1)
    GPIO.output(BUZZER_PIN, GPIO.HIGH)


# Only for standalone testing
if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    setup_buzzer()
    try:
        beep_success()
        time.sleep(1)
        beep_error()
    finally:
        GPIO.cleanup()
