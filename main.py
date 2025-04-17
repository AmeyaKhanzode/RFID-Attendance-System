import rfid_read
import display
import rfid_write
import RPi.GPIO as GPIO
import buzzer
import delete_attendance

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

buzzer.setup_buzzer()

print("Welcome to college!")

try:
    while True:
        try:
            print()
            choice = int(input(
                "Enter\n1 For viewing attendance\n2 For writing into the card\n3 For marking attendance\n4 To delete attendance (Teacher only)\n5 To exit\nChoice: "))

            if choice == 1:
                display.check_attendance()
            elif choice == 2:
                rfid_write.write()
            elif choice == 3:
                rfid_read.read()
            elif choice == 4:
                delete_attendance.delete()
            elif choice == 5:
                print("Exiting...")
                GPIO.cleanup()
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")

        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")

except KeyboardInterrupt:
    print()
    print("Exiting...")
    GPIO.cleanup()