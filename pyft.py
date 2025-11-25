import os
import sqlite3 as sql
import argparse
from components import *
import output

class PYFTParser(argparse.ArgumentParser):
    def error(self, message):
        output.error(message)
        self.exit(1)



# Helper functions for handling optional args
def parse_create(con: sql.Connection, comp: PYFTComponent, *args) -> None:
    obj = comp(args)
    obj.update_db(con)
    output.success(f"Created {comp.format_name} with name \"{comp.name}\".")

def parse_list(con: sql.Connection, comp: PYFTComponent) -> None: # TODO: Fix
    namemap = {"account": "accounts", "category": "categories", "entry": "entries"}
    cur = con.cursor()

    cur.execute(f"SELECT * FROM {namemap[comp.format_name]}")
    rows = cur.fetchall()

    if len(rows) == 0 or rows is None:
        output.error("No accounts found.")
    else:
        print(f"Found {len(rows)} accounts:")
        print("Placeholder") # Fix this also
        for r in rows:
            print("\t".join([str(x) for x in r])) # TODO: Format currency



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

            elif args.delete:
                accname = args.delete[0]

                cur.execute("SELECT * FROM accounts WHERE name = ?", (accname,))
                rows = cur.fetchone()

                if len(rows) == 0:
                    output.error(f"No account found with the name \"{accname}\".")
                else:
                    cur.execute("DELETE FROM accounts WHERE name = ?", (accname,))
                    output.success(f"Deleted account \"{accname}\".")



        case "category":
            if args.create:
                parse_create(con, Category, args.create)
        case "entry":
            print("Entry settings")
        case _:
            output.error("Unknown component. Must be \"account\", \"category\", or \"entry\"")

    con.commit()
    con.close()
