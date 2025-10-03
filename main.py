
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


class PomodoroTimer:
    def __init__(self, work_minutes, short_break_minutes, long_break_minutes, sessions_before_long_break):
        self.work_minutes = work_minutes
        self.short_break_minutes = short_break_minutes
        self.long_break_minutes = long_break_minutes
        self.sessions_before_long_break = sessions_before_long_break
        self.current_sesh = WorkSession(work_minutes)
        self.short_break_counter = 0
        
    def next_session(self):
        curr = self.current_sesh
        cname, cdurr = curr.get_name(), curr.get_duration()
        if cname == "Short Break" or cname == "Long Break":
            next_sesh = WorkSession(self.work_minutes)
        elif cname == "Work":
            if self.short_break_counter + 1 == self.sessions_before_long_break:
                next_sesh = LongBreak(self.long_break_minutes)
            else:
                next_sesh = ShortBreak(self.short_break_minutes)
                self.short_break_counter += 1
        self.current_sesh = next_sesh
        return curr

    def reset(self):
        self.current_sesh = WorkSession(self.work_minutes)
        self.short_break_counter = 0

    def plan(self, n_work_sessions):
        res = []
        for i in range(n_work_sessions):
            res.append(("Work", self.work_minutes))
            if (i + 1) % self.sessions_before_long_break == 0:
                res.append(("Long Break", self.long_break_minutes))
            else:
                res.append(("Short Break", self.short_break_minutes))
        return res
