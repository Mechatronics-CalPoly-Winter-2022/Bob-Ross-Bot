"""! 
@file servo.py

@brief A class that inherits from both the MotorDriver and 
EncoderDriver classes. Offers full functionality from both classes.
"""

from enc_driver import EncoderDriver, EncoderConfig
from motor_driver import MotorDriver, MotorConfig


class Servo(MotorDriver, EncoderDriver):
    '''!
    Class that combies the functionality of the encoder and motor drivers.
    '''

    gain: float
    name: str
    abs_pos: int
    _last_pos: int

    def __init__(self, name: str, m_config: MotorConfig, e_config: EncoderConfig) -> None:
        '''!
        Creates a servo object by initializing the motor and encoder drivers.
        @param m_config The motor configuration
        @param e_config The encoder configuration
        '''
        self.name = name
        MotorDriver.__init__(self, *m_config.args)
        EncoderDriver.__init__(self, *e_config.args)
        self.stop()
        EncoderDriver.zero(self)
        self.zero()

    def zero(self) -> None:
        '''!
        Sets the absolute position to 0.
        '''
        self.abs_pos = 0
        self._last_pos = 0

    def stop(self) -> None:
        '''!
        Stops the motor.
        '''
        MotorDriver.set_duty_cycle(self, 0)
        MotorDriver.disable_motor(self)

    def start(self, duty_cycle: float) -> None:
        '''!
        Starts the motor.
        @param duty_cycle The duty cycle to use for the motor
        '''
        MotorDriver.enable_motor(self)
        MotorDriver.set_duty_cycle(self, -duty_cycle)

    def update_position(self, direction: str) -> None:
        '''!
        Updates the absolute position of the servo.
        '''
        self._last_pos = self.abs_pos % self.MAX_VAL
        new_pos = EncoderDriver.read(self)
        
        if direction == 'positive':
            self.abs_pos += new_pos - self._last_pos
            if new_pos < self._last_pos:
                self.abs_pos += self.MAX_VAL
        elif direction == 'negative':
            self.abs_pos -= self._last_pos - new_pos
            if new_pos > self._last_pos:
                self.abs_pos -= self.MAX_VAL

        print(self._last_pos, new_pos, self.abs_pos)

    # def get_error(self, target: int) -> int:
    #     '''!
    #     Gets the error in the encoder.
    #     @param target The target position
    #     @return The error in the encoder
    #     '''
    #     if target
    #     return self.abs_pos - self._last_pos

    # def move_distance(self, dist: int) 
