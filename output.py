# File: output.py
# Date: 12/5/2025
# Authors:
# Mile Stojakovic
#     mstojako
#
# Team: 6
#
# ELECTRONIC SIGNATURE
# Mile Stojakovic
#
# The electronic signatures above indicate that the program
# submitted for evaluation is the combined effort of all
# team members and that each member of the team was an
# equal participant in its creation. In addition, each
# member of the team has a general understanding of
# all aspects of the program development and execution.
#
#  Version 1.0    Original    December 2025
# Helper functions for output and formatting

import datetime as dt
from termcolor import colored

def error(text, emoji=True) -> None:
    print(colored(f"{"❌" if emoji else ""} ERROR: {text}", "red"))

def warning(text, emoji=True) -> None:
    print(colored(f"{"⚠️" if emoji else ""}  WARNING: {text}", "yellow"))

def success(text, emoji=True) -> None:
    print(colored(f"{"✅" if emoji else ""} {text}", "green"))

def currency(num: float) -> str:
    norm = abs(num)
    numstr = str(int(norm))[::-1] # Convert number to string & reverse
    numstr = ",".join([numstr[i:i+3] for i in range(0, len(numstr), 3)]) # insert commas every 3 numbers
    numstr = ("-" if num < 0 else "") + "$" + numstr[::-1] + str(round(norm - int(norm), 2))[1:] # reverse again and add dollar sign and decimal
    return numstr

def str_to_date(text: str):
    match text.lower():
        case "today":
            return dt.date.today()
        case "yesterday":
            return dt.date.today() - dt.timedelta(days=1)
        case _:
            try:
                out = dt.datetime.strptime(text.lower(), "%m/%d/%Y")
                return out.date()
            except:
                error("Invalid date. Date should be in the format MM/DD/YYYY")
                warning("Date will be set to today.")
                return dt.date.today()

def hex_to_rgb(color: str) -> tuple[int, int, int]:
    if len(color) != 6:
        return (0, 0, 0)

    return (int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16))

# ACADEMIC INTEGRITY STATEMENT
# I have not used source code obtained from any other unauthorized
# source, either modified or unmodified.  Neither have I provided
# access to my code to another. The project I am submitting
# is my own original work.
