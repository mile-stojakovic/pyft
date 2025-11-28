import datetime as dt
from termcolor import colored

def error(text, emoji=True) -> None:
    print(colored(f"{"❌" if emoji else ""} ERROR: {text}", "red"))

def warning(text, emoji=True) -> None:
    print(colored(f"{"⚠️" if emoji else ""}  WARNING: {text}", "yellow"))

def success(text, emoji=True) -> None:
    print(colored(f"{"✅" if emoji else ""} {text}", "green"))

def currency(num: float) -> str:
    numstr = str(int(num))[::-1] # Convert number to string & reverse
    numstr = ",".join([numstr[i:i+3] for i in range(0, len(numstr), 3)]) # insert commas every 3 numbers
    numstr = "$" + numstr[::-1] + str(round(num - int(num), 2))[1:] # reverse again and add dollar sign and decimal
    return numstr

def str_to_date(text: str):
    match text.lower():
        case "tomorrow":
            return dt.date.today() + dt.timedelta(days=1)
        case "today":
            return dt.date.today()
        case _:
            try:
                out = dt.datetime.strptime(text.lower(), "%m/%d/%Y")
                return out.date()
            except:
                error("Invalid date. Date should be in the format MM/DD/YYYY")
                warning("Date will be set to today.")
                return dt.date.today()
