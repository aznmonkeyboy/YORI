import board
import pwmio
import digitalio

class motor_phase_enable:
    def __init__(self, enable_pin, phase_pin):
        self.enable_pin = enable_pin
        self.phase_pin = phase_pin
        self.enable = pwmio.PWMOut(self.enable_pin, duty_cycle=0, frequency=500)
        self.phase = digitalio.DigitalInOut(self.phase_pin)
        self.phase.direction = digitalio.Direction.OUTPUT
        self.phase.drive_mode = digitalio.DriveMode.PUSH_PULL

    def __init__(self, enable_pin, phase_pin, frequency):
        motor_phase_enable(enable_pin, phase_pin)
        self.frequency = frequency
        self.enable_ctrl.frequency = self.frequency

    def run(self, speed):
        # Speed is from -1 to 1
        # positive is CW
        # negative is CCW
        # max = 65535
        # min = 0
        self.enable.duty_cycle = int(speed * 65535)
        if speed >= 0:
            self.phase.pull = digitalio.Pull.UP
        else:
            self.phase.pull = digitalio.Pull.DOWN
                
class motor_pwm:
    def __init__(self, in1, in2):
        self.in1 = in1
        self.in2 = in2
        # frequency = 500 is default
        self.motor1 = pwmio.PWMOut(self.in1, duty_cycle=0, frequency=500)
        self.motor2 = pwmio.PWMOut(self.in2, duty_cycle=0, frequency=500)

    def __init__(self, in1, in2, frequency):
        motor_pwm(self, in1, in2)
        self.frequency = frequency
        self.motor1.frequency = self.frequency
        self.motor2.frequency = self.frequency

    def run(self, speed, mode):
        # Speed is from -1 to 1
        # positive is CW
        # negative is CCW
        on = 65535
        off = 0
        if mode == "coast":
            if speed >= 0:
                self.motor1.duty_cycle = int(speed * 65535)
                self.motor2.duty_cycle = off
            else:
                self.motor1.duty_cycle = off
                self.motor2.duty_cycle = int(-speed * 65535)
        elif mode == "brake":
            if speed >= 0:
                self.motor2.duty_cycle = int(65535 - speed * 65535)
                self.motor1.duty_cycle = on
            elif speed < 0:
                self.motor2.duty_cycle = on
                self.motor1.duty_cycle = int(65535 + speed * 65535)

