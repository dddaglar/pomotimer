from .pomodoro_timer import PomodoroTimer
from .logger import log_session
from .session_controller import SessionController
    

class PomodoroCLI:
    def __init__(self):
        print("Welcome to the Pomodoro Timer CLI!")
        self.timer = None

    def setup_timer(self):
        inp = input("Press Enter to use default Pomodoro settings (25 min work, 5 min short break, 15 min long break, 4 sessions before long break) or type 'custom' to set your own: ")
        if inp.strip().lower() != "custom":
            self.timer = PomodoroTimer(25, 5, 15, 4)
            print("Using default settings.")
        else:
            work = int(input("Enter work session duration (minutes): "))
            short_break = int(input("Enter short break duration (minutes): "))
            long_break = int(input("Enter long break duration (minutes): "))
            sessions_before_long = int(input("Enter number of work sessions before a long break: "))
            self.timer = PomodoroTimer(work, short_break, long_break, sessions_before_long)
        print("Timer setup complete!")


    def start_session(self):
        session = self.timer.current_sesh
        def log_helper(actual_minutes, skipped):
            if not skipped:
                print(f"Completed {session.get_name()} session of {session.get_duration()} minutes.")
            else:
                print(f"{session.get_name()} Session skipped after {actual_minutes:.2f} minutes!")
            log_session(session.get_name(), session.get_duration(), actual_minutes)
        controller = SessionController(session, log_helper)
        controller.runloop()


    def run(self):
        self.setup_timer()
        while True:
            cmd = input("Enter command (start, next, reset, plan, exit): ").strip().lower()
            if cmd == "start":
                print(f"Starting {self.timer.current_sesh.get_name()} session for {self.timer.current_sesh.get_duration()} minutes.")
                self.start_session()
                print(f"{self.timer.current_sesh.get_name()} session finished.")
            elif cmd == "next":
                self.timer.next_session()
                print(f"Next session: {self.timer.current_sesh.get_name()} for {self.timer.current_sesh.get_duration()} minutes.")
            elif cmd == "reset":
                self.timer.reset()
                print("Timer reset to initial work session.")
            elif cmd == "plan":
                n = int(input("Enter number of work sessions to plan: "))
                plan = self.timer.plan(n)
                for sess in plan:
                    print(f"{sess[0]}: {sess[1]} minutes")
            elif cmd == "exit":
                print("Exiting Pomodoro Timer CLI. Goodbye!")
                break
            else:
                print("Invalid command. Please try again.")
