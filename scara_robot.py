import numpy as np
import math
import RPi.GPIO as GPIO
import time
from typing import Tuple

class SCARARobot:
    """SCARA 機器人運動學與伺服馬達控制"""

    def __init__(self, L1: float, L2: float, z_range: Tuple[float, float], servo_pins: dict):
        self.L1 = L1
        self.L2 = L2
        self.z_min, self.z_max = z_range
        self.servo_pins = servo_pins

        GPIO.setmode(GPIO.BCM)
        self.servos = {}
        for name, pin in servo_pins.items():
            GPIO.setup(pin, GPIO.OUT)
            pwm = GPIO.PWM(pin, 50)
            pwm.start(0)
            self.servos[name] = pwm

    def angle_to_duty(self, angle: float) -> float:
        return 2 + (angle / 18)

    def set_servo_angle(self, name: str, angle: float):
        duty = self.angle_to_duty(angle)
        self.servos[name].ChangeDutyCycle(duty)
        time.sleep(0.3)
        self.servos[name].ChangeDutyCycle(0)

    def forward_kinematics(self, theta1: float, theta2: float, z: float) -> np.ndarray:
        x = self.L1 * math.cos(theta1) + self.L2 * math.cos(theta1 + theta2)
        y = self.L1 * math.sin(theta1) + self.L2 * math.sin(theta1 + theta2)
        return np.array([x, y, z])

    def inverse_kinematics(self, target_pos: np.ndarray) -> Tuple[float, float, float]:
        x, y, z = target_pos
        D = (x**2 + y**2 - self.L1**2 - self.L2**2) / (2 * self.L1 * self.L2)
        D = np.clip(D, -1.0, 1.0)
        theta2 = math.acos(D)
        beta = math.atan2(y, x)
        phi = math.atan2(self.L2 * math.sin(theta2), self.L1 + self.L2 * math.cos(theta2))
        theta1 = beta - phi
        z = np.clip(z, self.z_min, self.z_max)
        return theta1, theta2, z

    def move_to(self, target_pos: np.ndarray):
        theta1, theta2, z = self.inverse_kinematics(target_pos)
        self.set_servo_angle("theta1", math.degrees(theta1))
        self.set_servo_angle("theta2", math.degrees(theta2))
        self.set_servo_angle("z", z)

    def cleanup(self):
        for pwm in self.servos.values():
            pwm.stop()
        GPIO.cleanup()

