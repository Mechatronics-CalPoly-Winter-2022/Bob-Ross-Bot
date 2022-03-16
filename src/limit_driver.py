'''!
@file limit_driver.py
@brief A class that handles the limit switches.
'''

import pyb


class LimitSwitch:
    '''!
    Class that handles the limit switches.
    '''

    def __init__(self, out_pin, in_pin) -> None:
        '''!
        Creates a limit switch by initializing the GPIO pins.
        @param out_pin The pin to which the limit switch is connected
        @param in_pin The pin to which the limit switch is connected
        '''
        self._out_pin = pyb.Pin(out_pin, pyb.Pin.OUT_PP)
        self._out_pin.high()

        self._in_pin = pyb.Pin(in_pin, pyb.Pin.IN, pull=pyb.Pin.PULL_DOWN)

    def is_pressed(self) -> bool:
        '''!
        Checks if the limit switch is pressed.
        @return True if the limit switch is pressed, False otherwise
        '''
        return self._in_pin.value() == 1