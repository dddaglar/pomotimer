from enum import Enum

class SessionType(Enum):
    WORK = 0
    SHORT_BREAK = 1
    LONG_BREAK = 2

    def __str__(self) -> str:
        return self.name.replace("_", " ").title()
    
def session_type_default_duration(type: SessionType) -> int:
    defaults = [25,5,15]
    return defaults[type.value]


class TimerSession:
    def __init__(self, type: int, duration_minutes: int):
        self.type = type
        self.duration_minutes = duration_minutes

    @staticmethod
    def of_type_default(type: SessionType):
        duration_minutes = session_type_default_duration(type)
        return TimerSession(type.value, duration_minutes)
    
    @staticmethod
    def work(duration_minutes:int):
        return TimerSession(SessionType.WORK, duration_minutes)
    
    @staticmethod
    def short_break(duration_minutes:int):
        return TimerSession(SessionType.SHORT_BREAK, duration_minutes)
    
    @staticmethod
    def long_break(duration_minutes:int):
        return TimerSession(SessionType.LONG_BREAK, duration_minutes)

    def get_type(self) -> SessionType:
        return self.type

    def get_duration(self) -> int:
        return self.duration_minutes
    
    def next(self) -> SessionType:
        match self:
            case SessionType.WORK:
                return SessionType.SHORT_BREAK
            case SessionType.SHORT_BREAK | SessionType.LONG_BREAK:
                return SessionType.WORK