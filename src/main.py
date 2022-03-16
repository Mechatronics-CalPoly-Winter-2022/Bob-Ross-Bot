'''
PA10 - Wheel enable
PB4 - Wheel positive
PB5 - Wheel negative
PC6 - Wheel encoder B
PC7 - Wheel encoder A

~0-81000 encoder ticks
PC1 - Arm enable
PA0 - Arm positive
PA1 - Arm negative
PB6 - Arm encoder B
PB7 - Arm encoder A

PB9 - Solenoid

PA8 - Wheel limit power
PB10 - Wheel limit input

PA5 - Arm limit power
PA6 - Arm limit input
'''
import gc
import pyb
import cotask
import task_share
from task_share import Share
import utime
from enc_driver import EncoderConfig, EncoderDriver
from motor_driver import MotorConfig
from servo import Servo
from sol_driver import Solenoid
from limit_driver import LimitSwitch
from pid import PID


# serial comm
serial = pyb.USB_VCP()

# servo 1 (wheel)
m_config = MotorConfig('PA10', 'PB4', 'PB5', pyb.Timer(3))
e_config = EncoderConfig('PC6', 'PC7', pyb.Timer(8))
servo1 = Servo('servo1', m_config, e_config)
servo1.zero()

# sesrvo 2 (arm)
m_config = MotorConfig('PC1', 'PA0', 'PA1', pyb.Timer(5))
e_config = EncoderConfig('PB6', 'PB7', pyb.Timer(4))
servo2 = Servo('servo2', m_config, e_config)
servo2.zero()

sol = Solenoid('PB9')

lim_wheel = LimitSwitch('PB10', 'PA8')
lim_arm = LimitSwitch('PA5', 'PA6')

# initialize shares for the position task
pos1 = Share('i')
pos1.put(0)
pos2 = Share('i')
pos2.put(0)

# initialize shares for servo status
servo1_idle = Share('i')
servo1_idle.put(1)
servo2_idle = Share('i')
servo2_idle.put(1)


def go_to_pos(servo: Servo, pos: int, idle: Share):
    '''!
    Moves a servo to the given position.
    @param servo The servo to move
    @param pos The position to move to
    '''

    # we aren't already close enough
    if not (pos - 50 < servo.abs_pos < pos + 50):
        print('not close enough')
        # if we need to make multiple turns
        if abs(servo.abs_pos - pos) > servo.MAX_VAL:
            print('multiple turns')
            # go positive until pos - servo.MAX_VAL
            if servo.abs_pos > pos:
                print('positive')
                servo.start(100)
                while servo.abs_pos < pos - servo.MAX_VAL:
                    servo.update_position('positive')
                    yield(0)
            # go negative until pos + servo.MAX_VAL
            else:
                print('negative')
                servo.start(-100)
                while servo.abs_pos > pos + servo.MAX_VAL:
                    servo.update_position('negative')
                    yield(0)

        # now we are on our last leg so we use PID to get there
        print('last leg')
        setpoint = pos - servo.abs_pos
        pid = PID(setpoint, 0.1)

        # while we are more that 50 ticks away from our setpoint
        while not (pos - 50 < servo.abs_pos < pos + 50):
            pwm = pid.update(servo.get_error(setpoint))
            servo.start(pwm)
            servo.update_position('negative' if pwm > 0 else 'positive')
            yield(0)

    # we are close enough so stop
    print('finished')
    servo.stop()
    idle.put(1)
    print('done at', servo.abs_pos)


def task_go_to_pos1():
    '''!
    Moves servo 1 to the given position

    Needs servo1, pos1, and servo1_idle to be set
    '''
    # wait for servo 1 to be idle
    while True:
        if servo1_idle.get():
            break
        yield(0)

    # run the servo
    servo1_idle.put(0)
    gen = go_to_pos(servo1, pos1.get(), servo1_idle)
    while True:
        yield(next(gen))


def task_go_to_pos2():
    '''!
    Moves servo 2 to the given position

    Needs servo2, pos2, and servo2_idle to be set
    '''
    print('task_go_to_pos2')
    # wait for servo 2 to be idle
    while True:
        if servo2_idle.get():
            break
        yield(0)

    # run the servo
    servo2_idle.put(0)
    gen = go_to_pos(servo2, pos2.get(), servo2_idle)
    while True:
        yield(next(gen))

def main():

    # declare more variables here

    # center the arm

    try:
        # setup
        # go in to the limit
        servo2.start(100)
        while not lim_arm.is_pressed():
            pyb.delay(100)
        servo2.start(-100)
        pyb.delay(500)
        servo2.stop()
        servo2.zero()
        EncoderDriver.zero(servo1)

        counter = 0
        sol_status = 0
        # bounce between the limits
        servo2.start(-100)
        servo1.start(40)
        while True:
            if lim_arm.is_pressed():
                servo2.start(-100)
            elif lim_wheel.is_pressed():
                servo2.start(100)

            servo1_val = servo1.read()
            if servo1_val > 2000 and servo1_val < servo1.HALF_VAL:
                servo1.start(-40)
            elif servo1_val < servo1.MAX_VAL - 2000 and servo1_val > servo1.HALF_VAL:
                servo1.start(40)
            
            counter += 1
            if counter % 20 == 0:
                sol_status = ~sol_status
            if sol_status:
                sol.on()
            else:
                sol.off()
            pyb.delay(50)

    finally:
        servo1.stop()
        servo2.stop()
        sol.off()


if __name__ == "__main__":
    # turn off the solenoid
    pyb.Pin('PB9', pyb.Pin.OUT_PP).low()

    # don't run on boot for now
    # main()