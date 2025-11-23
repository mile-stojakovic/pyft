import sqlite3 as sql
import argparse
from components import *
import output

class PYFTParser(argparse.ArgumentParser):
    def error(self, message):
        output.error(message)
        self.exit(1)

parser = PYFTParser(prog="PYFT - Python Financial Tracker", description="A simple CLI-based financial tracker written in Python.")

parser.add_argument("context", help="The context in which to operate (account, category, or entry)")
parser.add_argument("-c", "--create", nargs="+", help="Creates a new instance of the context")

con = sql.connect(DB_NAME)

if __name__ == "__main__":
    args = parser.parse_args()

    match args.context:
        case "account":
            print("Account settings")
        case "category":
            print("Category settings")
        case "entry":
            print("Entry settings")
        case _:
            output.error("Unknown context. Must be \"account\", \"category\", or \"entry\"")

    con.commit()
    con.close()
