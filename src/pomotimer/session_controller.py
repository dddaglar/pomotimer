import time
import sys
import threading


class SessionController:
    def __init__(self, session, log_helper=None):
        self.session = session
        self.log_helper = log_helper
        self._skip_flag = False
        self._pause_event = threading.Event()
        self._pause_event.set()

        self.start_time = None
        self.total_paused = 0

    def print_progress_bar(self, remaining, total, name, bar_length=30):
        progress = total - remaining
        percent = progress / total
        mins, secs = divmod(remaining, 60)
        time_format = f"{mins:02}:{secs:02}"
        filled = int(bar_length * percent)
        bar = "█" * filled + "-" * (bar_length - filled)
        print(f"\r{name} [{bar}] {percent*100:5.1f}% - Time Left: {time_format}", end="")
        sys.stdout.flush()


    def get_remaining_time(self):
        now = time.monotonic()
        elapsed = now - self.start_time - self.total_paused
        remaining = max(int(self.session.get_duration() * 60) - elapsed, 0)
        mins, secs = divmod(remaining, 60)
        return mins, secs, remaining
        

    def _input_thread(self):
        while True:
            cmd = input().strip().lower()
            print(f"Received command: {cmd}")
            if cmd == "q":
                self._skip_flag = True
                break
            elif cmd == "p":
                if self._pause_event.is_set():
                    self._pause_event.clear()
                    mins, secs, _ = self.get_remaining_time()
                    print(f"\nPaused. Press 'r' to resume. {int(mins):02d}:{int(secs):02d} minutes left.")
            elif cmd == "r":
                if not self._pause_event.is_set():
                    self._pause_event.set()
                    print("\nResumed.")

    
    def runloop(self):
        total_seconds = int(self.session.get_duration() * 60)
        self._skip_flag = False
        self._pause_event.set()
        input_thread = threading.Thread(target=self._input_thread, daemon=True)
        input_thread.start()
        print("\nType 'q' to quit, 'p' to pause 'r' to resume the timer at any time.")

        self.start_time = time.monotonic()
        end = self.start_time + total_seconds
        seconds_spent = 0
        try:
            while not self._skip_flag and time.monotonic() < end:
                if not self._pause_event.is_set():
                    pause_start = time.monotonic()
                    self._pause_event.wait()
                    pause_duration = time.monotonic() - pause_start
                    end += pause_duration
                    self.total_paused += pause_duration
                remaining_seconds = int(end - time.monotonic())
                self.print_progress_bar(remaining_seconds, total_seconds, self.session.get_name())
                time.sleep(1)
                seconds_spent += 1
            actual_seconds = self.session.get_duration() * 60 - self.get_remaining_time()[2]
            actual_minutes = actual_seconds / 60
            print("\n")
            self.log_helper(actual_minutes, self._skip_flag)
        except KeyboardInterrupt:
            print("\nTimer interrupted. Exiting...")
            sys.exit(0)

    