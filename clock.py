class Clock:
    def __init__(self, timer_length):
        self.timer_length = timer_length
        self.time_left = 0

    def tick(self):
        if self.time_left < self.timer_length:
            self.time_left -= 1
        return self.time_left
