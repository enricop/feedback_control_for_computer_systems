class PidController:
    def __init__(self, kp, ki, kd=0):
        self.kp, self.ki, self.kd = kp, ki, kd
        self.i = 0
        self.d = 0
        self.prev = 0   # store the error of the previous step

    def work(self, e):
        """
        Here the factor DT represents the step length δt, which measures the
        interval between successive control actions, expressed in the units in
        which time is measured.
        """
        self.i += DT * e
        self.d = (e - self.prev) / DT
        self.prev = e

        return (self.kp * e) + (self.ki * self.i) + (self.kd * self.d)