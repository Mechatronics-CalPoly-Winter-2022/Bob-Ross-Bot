"""! 
@file sol_driver.py

@brief Controls a solenoid
"""

import pyb      # import the micropy library


class Solenoid:
    '''!
    Class that controls a solenoid.
    '''

    def __init__(self, ena: str) -> None:
        '''!
        Creates a solenoid by initializing the GPIO pin.
        @param ena The pin to which the solenoid is connected
        '''
        self._ena = pyb.Pin(ena, pyb.Pin.OUT_PP)
        self.off()

    def on(self) -> None:
        '''!
        Turns the solenoid on.
        '''
        self._ena.high()

    def off(self) -> None:
        '''!
        Turns the solenoid off.
        '''
        self._ena.low()