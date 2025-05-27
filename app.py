from flask import Flask, render_template, jsonify, request
import RPi.GPIO as GPIO
import time
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
# === GPIO SETUP ===
ARM_PIN = 12       # Elbow
GRIPPER_PIN = 13   # Gripper
SHOULDER_PIN = 18  # Shoulder

GPIO.setmode(GPIO.BCM)
GPIO.setup(ARM_PIN, GPIO.OUT)
GPIO.setup(GRIPPER_PIN, GPIO.OUT)
GPIO.setup(SHOULDER_PIN, GPIO.OUT)

arm_pwm = GPIO.PWM(ARM_PIN, 50)
gripper_pwm = GPIO.PWM(GRIPPER_PIN, 50)
shoulder_pwm = GPIO.PWM(SHOULDER_PIN, 50)

arm_pwm.start(0)
gripper_pwm.start(0)
shoulder_pwm.start(0)

# === HELPER FUNCTIONS ===
def set_servo_angle(pwm, angle, delay=0.5):
    duty = (angle / 18.0) + 2
    pwm.ChangeDutyCycle(duty)
    time.sleep(delay)
    pwm.ChangeDutyCycle(0)

def set_angle_slow(pwm, start_angle, end_angle, delay=0.02):
    step = 1 if end_angle > start_angle else -1
    for angle in range(start_angle, end_angle + step, step):
        duty = (angle / 18.0) + 2
        pwm.ChangeDutyCycle(duty)
        time.sleep(delay)
    pwm.ChangeDutyCycle(0)

# === ROUTES ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gripper/<action>', methods=['POST'])
def gripper_control(action):
    try:
        if action == 'open':
            set_servo_angle(gripper_pwm, 0)
            return jsonify({'status': 'Gripper opened'})
        elif action == 'close':
            set_servo_angle(gripper_pwm, 90)
            return jsonify({'status': 'Gripper closed'})
        else:
            return jsonify({'status': 'Invalid gripper action'}), 400
    except Exception as e:
        return jsonify({'status': f'Error: {e}'}), 500

@app.route('/shoulder/<direction>', methods=['POST'])
def shoulder_control(direction):
    global shoulder_angle
    try:
        if direction == 'increase':
            new_angle = min(180, shoulder_angle + 20)
        elif direction == 'decrease':
            new_angle = max(0, shoulder_angle - 20)
        else:
            return jsonify({'status': 'Invalid shoulder direction'}), 400

        set_angle_slow(shoulder_pwm, shoulder_angle, new_angle)
        shoulder_angle = new_angle
        return jsonify({'status': f'Shoulder moved to {shoulder_angle}°'})
    except Exception as e:
        return jsonify({'status': f'Error: {e}'}), 500

@app.route('/elbow/<direction>', methods=['POST'])
def elbow_control(direction):
    global elbow_angle
    try:
        if direction == 'increase':
            new_angle = min(180, elbow_angle + 20)
        elif direction == 'decrease':
            new_angle = max(0, elbow_angle - 20)
        else:
            return jsonify({'status': 'Invalid elbow direction'}), 400

        set_angle_slow(arm_pwm, elbow_angle, new_angle)
        elbow_angle = new_angle
        return jsonify({'status': f'Elbow moved to {elbow_angle}°'})
    except Exception as e:
        return jsonify({'status': f'Error: {e}'}), 500

@app.route('/shutdown', methods=['POST'])
def shutdown():
    arm_pwm.stop()
    gripper_pwm.stop()
    shoulder_pwm.stop()
    GPIO.cleanup()
    return jsonify({'status': 'System shutdown and GPIO cleaned'})

# === MAIN ===
if __name__ == '__main__':
    try:
        shoulder_angle = 160  # initial shoulder angle
        elbow_angle = 90      # initial elbow angle
        app.run(host='0.0.0.0', port=7000)
    except KeyboardInterrupt:
        arm_pwm.stop()
        gripper_pwm.stop()
        shoulder_pwm.stop()
        GPIO.cleanup()
