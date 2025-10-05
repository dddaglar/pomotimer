
class TimerSession:
    def __init__(self, name, duration_minutes):
        self.name = name
        self.duration_minutes = duration_minutes
        self.left = self.duration_minutes

    def get_name(self):
        return self.name

    def get_duration(self):
        return self.duration_minutes

    def get_remaining(self):
        return self.left

    def advance(self, minutes):
        if self.left - minutes <= 0: 
            self.left = 0
        else:
            self.left -= minutes
        
    def is_complete(self):
        return self.left == 0


class WorkSession(TimerSession):
    def __init__(self, duration_minutes):
        super().__init__("Work", duration_minutes)
        


class ShortBreak(TimerSession):
    def __init__(self, duration_minutes):
        super().__init__("Short Break", duration_minutes)


class LongBreak(TimerSession):
    def __init__(self, duration_minutes):
        super().__init__("Long Break", duration_minutes)