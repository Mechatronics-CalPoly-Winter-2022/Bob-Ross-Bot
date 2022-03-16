class PID:
    '''!
    Class that implements a PID controller.
    '''

    setpoint: int
    kp: float
    out_range: tuple

    def __init__(
        self, setpoint: int, kp: float = 0.1, out_range: tuple = (-100, 100, 30)
            ) -> None:
        '''!
        Creates a PID object.
        @param setpoint The desired setpoint
        @param kp The proportional gain
        @param out_range The output range
        '''
        self.setpoint = setpoint
        self.kp = kp
        self.out_range = out_range

    def set_setpoint(self, new: int) -> None:
        '''!
        Sets the new setpoint.
        @param new The new setpoint
        '''
        self.setpoint = new

    def update(self, error: int) -> int:
        '''!
        Updates the PID controller.
        @param error The current error
        @return The new duty cycle
        '''
        # calculate the proportional term
        p = self.kp * error

        p = max(min(p, self.out_range[1]), self.out_range[0])
        if p > 0 and p < self.out_range[2]:
            p = self.out_range[2]
        if p < 0 and p > -self.out_range[2]:
            p = -self.out_range[2]

        # return the PID output
        return p
