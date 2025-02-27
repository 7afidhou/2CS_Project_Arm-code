import RPi.GPIO as GPIO
import time

# Pin configuration
SERVO_1_PIN = 14  # GPIO 17 (Pin 11)
SERVO_2_PIN = 15  # GPIO 18 (Pin 12)

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_1_PIN, GPIO.OUT)
GPIO.setup(SERVO_2_PIN, GPIO.OUT)

# Set PWM frequency (50Hz)
servo1 = GPIO.PWM(SERVO_1_PIN, 50)
servo2 = GPIO.PWM(SERVO_2_PIN, 50)

# Start PWM with 0 degree position
servo1.start(0)
servo2.start(0)

# Function to move the servo
def set_angle(servo, angle):
    duty_cycle = 2 + (angle / 18)  # Convert angle to duty cycle
    servo.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)  # Stop signal to prevent jitter

try:
    # Move servos to 0°, 90°, and 180° then stop
    set_angle(servo1, 0)
    set_angle(servo2, 0)
    time.sleep(1)

    set_angle(servo1, 90)
    set_angle(servo2, 90)
    time.sleep(1)

finally:
    print("Cleaning up GPIO...")
    servo1.stop()
    servo2.stop()
    GPIO.cleanup()