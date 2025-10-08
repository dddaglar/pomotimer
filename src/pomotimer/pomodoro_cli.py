from .pomodoro_timer import PomodoroTimer
from .logger import log_session
from .session_controller import SessionController
    

class PomodoroCLI:
    def __init__(self, timer: PomodoroTimer):
        print("Welcome to the Pomodoro Timer CLI!")
        self.timer = timer

    def start_session(self):
        session = self.timer.current_sesh
        def log_helper(actual_minutes, skipped):
            if not skipped:
                print(f"Completed {session.get_type()} session of {session.get_duration()} minutes.")
            else:
                print(f"{session.get_type()} Session skipped after {actual_minutes:.2f} minutes!")
            log_session(str(session.get_type()), session.get_duration(), actual_minutes)
        controller = SessionController(session, log_helper)
        controller.runloop()


    def run(self):
        while True:
            cmd = input("Enter command (start, next, reset, plan, exit): ").strip().lower()
            if cmd == "start":
                print(f"Starting {self.timer.current_sesh.get_type()} session for {self.timer.current_sesh.get_duration()} minutes.")
                self.start_session()
                print(f"{self.timer.current_sesh.get_type()} session finished.")
            elif cmd == "next":
                self.timer.next_session()
                print(f"Next session: {self.timer.current_sesh.get_type()} for {self.timer.current_sesh.get_duration()} minutes.")
            elif cmd == "reset":
                self.timer.reset()
                print("Timer reset to initial work session.")
            elif cmd == "plan":
                n = int(input("Enter number of work sessions to plan: "))
                plan = self.timer.plan(n)
                print(self.timer.print_plan(plan))
            elif cmd == "exit":
                print("Exiting Pomodoro Timer CLI. Goodbye!")
                break
            else:
                print("Invalid command. Please try again.")
