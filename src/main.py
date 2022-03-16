"""!
@file main.py
@brief This file sets up the main loop and starts the tasks

@author Kyle Jennings, Zarek Lazowski, William Dorosk
@date 2022-Mar-8
"""

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
import pyb
from task_share import Share
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

# servo 2 (arm)
m_config = MotorConfig('PC1', 'PA0', 'PA1', pyb.Timer(5))
e_config = EncoderConfig('PB6', 'PB7', pyb.Timer(4))
servo2 = Servo('servo2', m_config, e_config)
servo2.zero()

sol = Solenoid('PB9')

# limit switch at the arm end and the wheel end
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


# UNUSED
# This task would have told a motor to move to a certain position
# def go_to_pos(servo: Servo, pos: int, idle: Share):
#     '''!
#     Moves a servo to the given position.
#     @param servo The servo to move
#     @param pos The position to move to
#     '''

#     # we aren't already close enough
#     if not (pos - 50 < servo.abs_pos < pos + 50):
#         print('not close enough')
#         # if we need to make multiple turns
#         if abs(servo.abs_pos - pos) > servo.MAX_VAL:
#             print('multiple turns')
#             # go positive until pos - servo.MAX_VAL
#             if servo.abs_pos > pos:
#                 print('positive')
#                 servo.start(100)
#                 while servo.abs_pos < pos - servo.MAX_VAL:
#                     servo.update_position('positive')
#                     yield(0)
#             # go negative until pos + servo.MAX_VAL
#             else:
#                 print('negative')
#                 servo.start(-100)
#                 while servo.abs_pos > pos + servo.MAX_VAL:
#                     servo.update_position('negative')
#                     yield(0)

#         # now we are on our last leg so we use PID to get there
#         print('last leg')
#         setpoint = pos - servo.abs_pos
#         pid = PID(setpoint, 0.1)

#         # while we are more that 50 ticks away from our setpoint
#         while not (pos - 50 < servo.abs_pos < pos + 50):
#             pwm = pid.update(servo.get_error(setpoint))
#             servo.start(pwm)
#             servo.update_position('negative' if pwm > 0 else 'positive')
#             yield(0)

#     # we are close enough so stop
#     print('finished')
#     servo.stop()
#     idle.put(1)
#     print('done at', servo.abs_pos)


# UNUSED
# This task would have used the go_to_pos task with servo1 (wheel)
# def task_go_to_pos1():
#     '''!
#     Moves servo 1 to the given position

#     Needs servo1, pos1, and servo1_idle to be set
#     '''
#     # wait for servo 1 to be idle
#     while True:
#         if servo1_idle.get():
#             break
#         yield(0)

#     # run the servo
#     servo1_idle.put(0)
#     gen = go_to_pos(servo1, pos1.get(), servo1_idle)
#     while True:
#         yield(next(gen))


# UNUSED
# This task would have used the go_to_pos task with servo2 (arm)
# def task_go_to_pos2():
#     '''!
#     Moves servo 2 to the given position

#     Needs servo2, pos2, and servo2_idle to be set
#     '''
#     print('task_go_to_pos2')
#     # wait for servo 2 to be idle
#     while True:
#         if servo2_idle.get():
#             break
#         yield(0)

#     # run the servo
#     servo2_idle.put(0)
#     gen = go_to_pos(servo2, pos2.get(), servo2_idle)
#     while True:
#         yield(next(gen))

def main():
    try:
        # move inwards to the limit switch
        servo2.start(100)
        while not lim_arm.is_pressed():
            pyb.delay(100)

        # back off a little bit
        servo2.start(-100)
        pyb.delay(500)
        servo2.stop()

        # zero at the backed off distance, that way we don't go too far back
        servo2.zero()
        EncoderDriver.zero(servo1)

        # bounce between the limits
        counter = 0
        sol_status = 0
        
        # start by moving the arm left and the carriage outwards
        servo2.start(-100)
        servo1.start(40)

        # continue to bounce off the limits forever
        while True:
            # inward limit
            if lim_arm.is_pressed():
                servo2.start(-100)
            # outward limit
            elif lim_wheel.is_pressed():
                servo2.start(100)

            servo1_val = servo1.read()
            # left limit
            if servo1_val > 2000 and servo1_val < servo1.HALF_VAL:
                servo1.start(-40)
            # right limit
            elif servo1_val < servo1.MAX_VAL - 2000 and servo1_val > servo1.HALF_VAL:
                servo1.start(40)
            
            # alternate the solenoid every second-ish
            counter += 1
            if counter % 20 == 0:
                sol_status = ~sol_status
            if sol_status:
                sol.on()
            else:
                sol.off()
            
            # delay 50ms before checking again
            pyb.delay(50)

    finally:
        # make sure to turn everything off
        servo1.stop()
        servo2.stop()
        sol.off()


if __name__ == "__main__":
    # turn off the solenoid
    pyb.Pin('PB9', pyb.Pin.OUT_PP).low()

    # don't run on boot for now
    main()