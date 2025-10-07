from .timer_session import WorkSession, ShortBreak, LongBreak

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