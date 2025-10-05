from .pomodoro_timer import PomodoroTimer
import time
import sys
import threading

class PomodoroCLI:
    def __init__(self):
        print("Welcome to the Pomodoro Timer CLI!")
        self.timer = None
        self._skip_flag = False

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

    def _input_thread(self):
        while True:
            cmd = input().strip().lower()
            print(f"Received command: {cmd}")
            if cmd == "q":
                self._skip_flag = True
                break

    def countdown(self):
        session = self.timer.current_sesh
        total_seconds = int(session.get_remaining() * 60)
        self._skip_flag = False
        input_thread = threading.Thread(target=self._input_thread, daemon=True)
        input_thread.start()
        print("\nType 'q' to quit the timer at any time.")
        seconds_spent = 0
        try:
            while total_seconds > 0 and not self._skip_flag:
                mins, secs = divmod(total_seconds, 60)
                time_format = f"{mins:02}:{secs:02}"
                print(f"\r{session.get_name()} - Time Left: {time_format}", end="")
                time.sleep(1)
                total_seconds -= 1
                seconds_spent += 1
                session.advance(1/60)
            print("\n")
            if self._skip_flag:
                mins_spent = seconds_spent // 60
                mins_left = total_seconds // 60
                print(f"Session skipped! You spent {mins_spent} min {seconds_spent%60} sec. Skipped {mins_left} min {total_seconds%60} sec.")
            else:
                print(f"Completed {session.get_name()} session of {session.get_duration()} minutes.")
        except KeyboardInterrupt:
            print("\nTimer interrupted. Exiting...")
            sys.exit(0)


    def run(self):
        self.setup_timer()
        while True:
            cmd = input("Enter command (start, next, reset, plan, exit): ").strip().lower()
            if cmd == "start":
                print(f"Starting {self.timer.current_sesh.get_name()} session for {self.timer.current_sesh.get_duration()} minutes.")
                self.countdown()
                print(f"{self.timer.current_sesh.get_name()} session finished.")
            elif cmd == "next":
                completed_session = self.timer.next_session()
                if completed_session.get_duration() == completed_session.get_remaining():
                    print(f"Skipped {completed_session.get_name()} session of {completed_session.get_duration()}.")
                else:
                    print(f"Finished {completed_session.get_name()} session of {completed_session.get_duration() - completed_session.get_remaining()} minutes.")
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