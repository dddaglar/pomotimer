from .pomodoro_cli import PomodoroCLI


def main():
    cli = PomodoroCLI()
    cli.run()

if __name__ == "__main__":
    main()