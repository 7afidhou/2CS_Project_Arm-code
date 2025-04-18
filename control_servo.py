import RPi.GPIO as GPIO
import time

# Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setup(9, GPIO.OUT)

# PWM à 50Hz
pwm = GPIO.PWM(9, 50)
pwm.start(0)

# Mouvement fluide
def set_angle_slow(start_angle, end_angle, delay=0.02):
    step = 1 if end_angle > start_angle else -1
    for angle in range(start_angle, end_angle + step, step):
        duty = (angle / 18) + 2
        pwm.ChangeDutyCycle(duty)
        time.sleep(delay)

try:
    print("→ Rotation vers 0°")
    set_angle_slow(90, 0)
    time.sleep(1)

    print("→ Rotation vers 90°")
    set_angle_slow(0, 90)
    time.sleep(1)

    print("→ Rotation vers 180°")
    set_angle_slow(90, 180)
    time.sleep(1)

finally:
    pwm.stop()
    GPIO.cleanup()
