from .pomodoro_cli import PomodoroCLI
from .pomodoro_timer import PomodoroTimer, TimerConfig, prompt_timer_config


def main():
    timer_config = prompt_timer_config()
    timer = PomodoroTimer(timer_config)
    cli = PomodoroCLI(timer)

    cli.run()

if __name__ == "__main__":
    main()