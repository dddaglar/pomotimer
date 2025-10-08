#from .timer_session import WorkSession, ShortBreak, LongBreak
from timeit import Timer
from .timer_session import SessionType, TimerSession

class TimerConfig:
    def __init__(self, work_duration=25, short_break=5, long_break=15, sessions_before_long=4):
        self.work_duration = work_duration
        self.short_break = short_break
        self.long_break = long_break
        self.sessions_before_long = sessions_before_long

    #maybe include a static method

def prompt_timer_config()->TimerConfig:
    inp = input("Press Enter to use default Pomodoro settings (25 min work, 5 min short break, 15 min long break, 4 sessions before long break) or type 'custom' to set your own: ")
    if inp.strip().lower() != "custom":
        print("Using default settings.")
        return TimerConfig()
    work = int(input("Enter work session duration (minutes): "))
    short_break = int(input("Enter short break duration (minutes): "))
    long_break = int(input("Enter long break duration (minutes): "))
    sessions_before_long = int(input("Enter number of work sessions before a long break: "))
    print("Timer setup complete!")
    return TimerConfig(
        work_duration=work,
        short_break = short_break,
        long_break=long_break,
        sessions_before_long=sessions_before_long
    )


class PomodoroTimer:
    def __init__(self, config: TimerConfig):
        self.config = config
        self.current_sesh = TimerSession.work(self.config.work_duration)
        self.short_break_counter = 0
        self.durations = [self.config.work_duration, self.config.short_break, self.config.long_break]

    def keep_track_of_breaks(self, next_session_type: SessionType)->SessionType:
        if next_session_type == SessionType.SHORT_BREAK:
            if self.short_break_counter + 1 == self.config.sessions_before_long:
                next_session_type = SessionType.LONG_BREAK
            else:
                self.short_break_counter += 1
        return next_session_type
    
    def next_session(self):
        curr = self.current_sesh
        cur_sess_type = curr.get_type()
        next_session_type = cur_sess_type.next() #will make sense on timer_session.py
        next_session_type = self.keep_track_of_breaks(next_session_type)
        next_session_duration = self.durations[next_session_type.value]

        self.current_sesh = TimerSession(next_session_type, next_session_duration)
        

    def reset(self):
        self.current_sesh = TimerSession.work(self.config.work_duration)
        self.short_break_counter = 0

    def plan(self, n_work_sessions):
        res = ([TimerSession.work(self.config.work_duration), 
               TimerSession.short_break(self.config.short_break)] * (n_work_sessions-1)) + [TimerSession.work(self.config.work_duration)]
        longs = self.config.sessions_before_long
        freq = (longs * 2-1)
        for i in range(freq, len(res), freq):
            res[i] = TimerSession.long_break(self.config.long_break)
        return res
    
    def print_plan(self, plan):
        res_str = []
        for i, sesh in enumerate(plan):
            res_str.append(f"{i+1}. {sesh.get_type()} Session of Length: {sesh.get_duration()}")
        return "\n".join(res_str)