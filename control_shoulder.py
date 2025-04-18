import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(10, GPIO.OUT)

pwm = GPIO.PWM(10, 50)
pwm.start(0)

def set_angle_slow(servo_pwm, start_angle, end_angle):
    step = 1 if end_angle > start_angle else -1
    for angle in range(start_angle, end_angle + step, step):
        duty_cycle = (angle / 18) + 2
        servo_pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.02)  # délai entre chaque petit mouvement

try:
    set_angle_slow(pwm, 0, 90)    # Aller doucement de 0° à 90°
    time.sleep(1)
    set_angle_slow(pwm, 90, 180)  # Puis 90° à 180°
    time.sleep(1)
    set_angle_slow(pwm, 180, 0)   # Retour à 0°

finally:
    pwm.stop()
    GPIO.cleanup()

