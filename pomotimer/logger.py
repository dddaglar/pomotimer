import json
from datetime import datetime

LOG_FILE = "pomodoro_sessions.jsonl"

def log_session(session_type, planned_duration, actual_duration):
    entry = {
        "date": "{:%Y-%m-%d}".format(datetime.now()),
        "start_time": datetime.now().isoformat(),
        "session_type": session_type,
        "planned_duration": planned_duration,
        "actual_duration": actual_duration
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")