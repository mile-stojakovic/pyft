import os
import sqlite3 as sql
import argparse
from termcolor import colored
from components import *
import output

namemap = {"account": "accounts", "category": "categories", "entry": "entries"}

class PYFTParser(argparse.ArgumentParser):
    def error(self, message):
        output.error(message)
        self.exit(1)



# Helper functions for handling optional args
def parse_create(con: sql.Connection, comp: PYFTComponent, *args) -> None:
    obj = None

    try:
        obj = comp(*(args[0])) # call constructor
    except TypeError: # In case too many args were given to the constructor
        match comp.format_name:
            case "category":
                output.error("Expected 2 arguments (name, color).")
            case "account":
                output.error("Expected 2 arguments (name, balance).")
            case "entry":
                output.error("Expected 5 arguments (name, amount, category, account, date).")
        return

    obj.update_db(con)
    output.success(f"Created {obj.format_name} with name \"{obj.name}\".")


def parse_list(con: sql.Connection, comp: PYFTComponent) -> None:
    objname = ""

    try:
        objname = namemap[comp.format_name]
    except KeyError:
        output.error(f"Invalid component \"{comp.format_name}\".")
        return

    cur = con.cursor()

    cur.execute(f"SELECT * FROM {objname}")
    rows = cur.fetchall()

    if len(rows) == 0 or rows is None:
        output.error(f"No {objname} found.")
    else:
        print(f"Found {len(rows)} {objname}:")
        print("Placeholder") # Fix this also
        for r in rows:
            for elem in r:
                if isinstance(elem, float) or isinstance(elem, int):
                    print(colored(output.currency(elem), ("green" if elem > 0 else "red")), end="") # TODO: Fix tabs
                else:
                    print(elem, end="")
                print("\t", end="")
            print()


def parse_delete(con: sql.Connection, comp: PYFTComponent, *args) -> None:
    objname = namemap[comp.format_name]
    accname = args[0][0]

    cur.execute(f"SELECT * FROM {objname} WHERE name = ?", (accname,))
    rows = cur.fetchone()

    if len(rows) == 0:
        output.error(f"No {comp.format_name} found with the name \"{accname}\".")
    else:
        cur.execute(f"DELETE FROM {objname} WHERE name = ?", (accname,))
        output.success(f"Deleted {comp.format_name} \"{accname}\".")



parser = PYFTParser(prog="pyft", description="A simple CLI-based financial tracker written in Python.")

parser.add_argument("component", help="The component in which to operate (account, category, or entry)")
parser.add_argument("-c", "--create", nargs="+", help="Create a new instance of the component", metavar="ARG")
parser.add_argument("-l", "--list", action="store_true", help="List information about accounts, entries, or categories")
parser.add_argument("-d", "--delete", nargs=1, help="Deletes a component by name", metavar="NAME")

con = sql.connect(DB_NAME)
cur = con.cursor()

if __name__ == "__main__":
    if not os.path.exists(DB_NAME):
        output.warning("No database file has been found. PYFT will not work without a database file. Would you like to create one? (y/n)")
        will_create = input()
        if will_create.lower() == "y":
            init_db()
            output.success("Initialized database file.")

    args = parser.parse_args()

    match args.component:
        case "account":
            if args.create:
                parse_create(con, Account, args.create)

            if args.list:
                parse_list(con, Account)

            if args.delete:
                parse_delete(con, Account, args.delete)


        case "category":
            if args.create:
                parse_create(con, Category, args.create)

            if args.list:
                parse_list(con, Category)

            if args.delete:
                parse_delete(con, Category, args.delete)


        case "entry":
            if args.create:
                parse_create(con, Entry, args.create)

            if args.list:
                parse_list(con, Entry)

            if args.delete:
                parse_delete(con, Entry, args.delete)


        case _:
            output.error("Unknown component. Must be \"account\", \"category\", or \"entry\"")

    con.commit()
    con.close()
