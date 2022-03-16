"""! 
@brief Controls a solenoid
"""

import pyb      # import the micropy library


class Solenoid:

    def __init__(self, ena: str) -> None:
        self._ena = pyb.Pin(ena, pyb.Pin.OUT_PP)
        self.off()

    def on(self) -> None:
        self._ena.high()

    def off(self) -> None:
        self._ena.low()