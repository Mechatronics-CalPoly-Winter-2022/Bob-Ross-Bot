import pyb


class LimitSwitch:

    def __init__(self, out_pin, in_pin) -> None:
        self._out_pin = pyb.Pin(out_pin, pyb.Pin.OUT_PP)
        self._out_pin.high()

        self._in_pin = pyb.Pin(in_pin, pyb.Pin.IN, pull=pyb.Pin.PULL_DOWN)

    def is_pressed(self) -> bool:
        return self._in_pin.value() == 1