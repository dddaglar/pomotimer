import time
import sys
import threading


class SessionController:
    def __init__(self, session, log_helper=None):
        self.session = session
        self.log_helper = log_helper
        self.quit = False
        self._pause_event = threading.Event()
        self._pause_event.set()

        self.start_time = None
        self.total_paused = 0
        self.pause_start = 0

    def print_progress_bar(self, remaining, total, name, bar_length=30):
        progress = total - remaining
        percent = progress / total
        mins, secs = divmod(remaining, 60)
        time_format = f"{mins:02}:{secs:02}"
        filled = int(bar_length * percent)
        bar = "█" * filled + "-" * (bar_length - filled)
        print(f"\r{name} [{bar}] {percent*100:5.1f}% - Time Left: {time_format}" , end="")
        sys.stdout.flush()


    def get_remaining_time(self):
        now = time.monotonic()
        elapsed = now - self.start_time - self.total_paused
        remaining = max(int(self.session.get_duration() * 60) - elapsed, 0)
        mins, secs = divmod(remaining, 60)
        return mins, secs, remaining
        

    def _input_thread(self):
        while True:
            cmd = input("").strip().lower()
            if cmd == "q":
                self.quit = True
                break
            if cmd == "p" and self._pause_event.is_set():
                mins, secs, _ = self.get_remaining_time()
                self._pause_event.clear()
                print(f"\nPaused. Press 'r' to resume. {int(mins):02d}:{int(secs):02d} minutes left.")
            elif cmd == "r" and not self._pause_event.is_set():
                self._pause_event.set()
                print("\nResumed.")
            else:
                continue

    
    def pause_handler(self):
        if self._pause_event.is_set() and self.pause_start != 0:
            #if we are resuming from a pause, calculate the duration
            pause_duration = time.monotonic() - self.pause_start
            self.total_paused += pause_duration
            self.pause_start = 0
        elif (self._pause_event.is_set() and self.pause_start == 0)  or (not self._pause_event.is_set() and self.pause_start != 0):
            #if we are in a consistent state, do nothing
            return
        elif not self._pause_event.is_set() and self.pause_start == 0: 
            #if we are just starting the pausing, set the pause start time
            self.pause_start = time.monotonic()
        return 0.0

    def calculate_remaining(self):
        _, _, remaining_total_secs = self.get_remaining_time()
        actual_seconds = self.session.get_duration() * 60 - remaining_total_secs
        actual_minutes = actual_seconds / 60
        return actual_minutes, remaining_total_secs

    
    def runloop(self):
        total_seconds = int(self.session.get_duration() * 60)
        self.quit = False
        self._pause_event.set()
        input_thread = threading.Thread(target=self._input_thread, daemon=True)
        input_thread.start()
        print("\nType 'q' to quit, 'p' to pause 'r' to resume the timer at any time.")

        next_tick = self.start_time = time.monotonic()
        end = self.start_time + total_seconds
        actual_minutes = 0
        try:
            while not self.quit and time.monotonic() < end:
                if time.monotonic() > next_tick:
                    next_tick += 1
                    delta = self.pause_handler()
                    if delta:
                        end += delta
                        next_tick += delta
                    if self._pause_event.is_set():
                        actual_minutes, remaining_seconds = self.calculate_remaining()
                        self.print_progress_bar(int(remaining_seconds), int(total_seconds), self.session.get_type())
            print("\n")
            self.log_helper(actual_minutes, self.quit)
        except KeyboardInterrupt:
            print("\nTimer interrupted. Exiting...")
            sys.exit(0)

    