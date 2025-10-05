
class TimerSession:
    def __init__(self, name, duration_minutes):
        self.name = name
        self.duration_minutes = duration_minutes

    def get_name(self):
        return self.name

    def get_duration(self):
        return self.duration_minutes


class WorkSession(TimerSession):
    def __init__(self, duration_minutes):
        super().__init__("Work", duration_minutes)
        


class ShortBreak(TimerSession):
    def __init__(self, duration_minutes):
        super().__init__("Short Break", duration_minutes)


class LongBreak(TimerSession):
    def __init__(self, duration_minutes):
        super().__init__("Long Break", duration_minutes)