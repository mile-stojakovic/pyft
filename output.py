from termcolor import colored

def error(text, emoji=True) -> None:
    print(colored(f"{"❌" if emoji else ""} ERROR: {text}", "red"))

def warning(text, emoji=True) -> None:
    print(colored(f"{"⚠️" if emoji else ""}  WARNING: {text}", "yellow"))

def success(text, emoji=True) -> None:
    print(colored(f"{"✅" if emoji else ""} {text}", "green"))
