# File: pyft.py
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
# Main program logic for PYFT

import sqlite3 as sql
import numpy as np
import argparse
from termcolor import colored
from components import *
import output

namemap = {"account": "accounts", "category": "categories", "entry": "entries"}

# Custom parser class, only used to customize error handling
class PYFTParser(argparse.ArgumentParser):
    def error(self, message):
        output.error(message)
        self.exit(1)



# Helper functions for handling optional args
# Returns true/false depending on whether the created component is a duplicate of a pre-existing one
def parse_create(con: sql.Connection, comp: PYFTComponent, *args) -> bool:
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
        return False

    res = obj.update_db(con)
    output.success(f"Created {obj.format_name} with name \"{obj.name}\".")
    return res


def parse_list(con: sql.Connection, comp: PYFTComponent) -> None:
    objname = ""

    try:
        objname = namemap[comp.format_name]
    except KeyError:
        output.error(f"Invalid component \"{comp.format_name}\".")
        return

    cur = con.cursor()


    if objname == "entries":
        cur.execute("SELECT * FROM entries ORDER BY date DESC")
    else:
        cur.execute(f"SELECT * FROM {objname}")


    rows = cur.fetchall()


    if len(rows) == 0 or rows is None:
        output.error(f"No {objname} found.")
    else:
        print(f"Found {len(rows)} {objname}:")

        match objname:
            case "accounts":
                print(colored(f"{"Account Name":<16}{"Balance":<24}", attrs=["bold"]))
            case "categories":
                print(colored(f"{"Category Name":<15}{"Color":<16}", attrs=["bold"]))
            case "entries":
                print(colored(f"{"Name":<16}{"Account":<16}{"Amount":<15}{"Date":<16}{"Category":<16}", attrs=["bold"]))
            case _:
                print("Placeholder")


        for r in rows:

            for index, elem in enumerate(r):

                if isinstance(elem, float) or isinstance(elem, int):
                    print(f"{colored(output.currency(elem), ("green" if elem > 0 else "red")):<24}", end="")
                else:
                    if objname == "categories":
                        print(colored(f"{elem:<15}", output.hex_to_rgb(r[1])), end="") # TODO: convert hex to rgb
                    # check if an entry is being printed and color the name and category name
                    elif objname == "entries" and (index == 0 or index == 4):
                        cur.execute("SELECT color FROM categories WHERE name = ?", (r[4],))
                        color = cur.fetchone()
                        print(colored(f"{elem:<16}", output.hex_to_rgb(color[0])), end="")
                    else:
                        print(f"{elem:<16}", end="")

            print()


def parse_delete(con: sql.Connection, comp: PYFTComponent, *args) -> None:
    objname = namemap[comp.format_name]
    accname = args[0][0]

    cur.execute(f"SELECT * FROM {objname} WHERE name = ?", (accname,))
    rows = cur.fetchone()

    if rows is None or len(rows) == 0:
        output.error(f"No {comp.format_name} found with the name \"{accname}\".")
    else:
        # Delete all entries with the account or category being deleted
        if objname == "accounts" or objname == "categories":
            output.warning(f"All entries with the {comp.format_name} name \"{accname}\" will be deleted. Proceed? (y/n)")

            confirm = input().lower() == "y"

            if not confirm:
                return

            cur.execute(f"DELETE FROM entries WHERE {"accountname" if objname == "accounts" else "category"} = ?", (accname,))


        cur.execute(f"DELETE FROM {objname} WHERE name = ?", (accname,))
        output.success(f"Deleted {comp.format_name} \"{accname}\".")




# Instantiate parser
parser = PYFTParser(prog="pyft", description="A simple CLI-based financial tracker written in Python.")

parser.add_argument("component", help="The component in which to operate (account, category, or entry)")

main_group = parser.add_argument_group("component options", "Main options for interfacing with components")

main_args = main_group.add_mutually_exclusive_group()

main_args.add_argument("-c", "--create", nargs="+", help="Create a new instance of the component", metavar="ARG")
main_group.add_argument("--exempt", action="store_true", help="Tells PYFT to not modify an account's balance based on the amount of a created entry")
main_args.add_argument("-l", "--list", action="store_true", help="List information about accounts, entries, or categories")
main_args.add_argument("-d", "--delete", nargs=1, help="Deletes a component by name", metavar="NAME")
main_args.add_argument("-s", "--summary", nargs=1, help="View a statistical summary of entries for a specific account", metavar="ACCOUNT")



# Instantiate database connection
con = sql.connect(DB_NAME)
cur = con.cursor()



# Main program logic
if __name__ == "__main__":
    with open(DB_NAME, "rb") as f:
        if len(f.readlines()) == 0:
            output.warning("No database file detected. PYFT will automatically create one.")
            init_db()

    args = parser.parse_args()

    match args.component:
        case "account":
            if args.create:
                parse_create(con, Account, args.create)

            if args.list:
                parse_list(con, Account)

            if args.delete:
                parse_delete(con, Account, args.delete)

            if args.summary:
                accname = args.summary[0]
                cur.execute("SELECT amount, category FROM entries WHERE accountname = ? ORDER BY amount DESC", (accname,))
                res = cur.fetchall()

                if res is None or len(res) == 0:
                    output.error(f"Account \"{accname}\" has no entries.")
                else:
                    amounts = [e[0] for e in res]
                    credits = [x for x in amounts if x > 0]
                    debits = [x for x in amounts if x < 0]

                    print(colored(f"Financial summary of {accname}", attrs=["bold"]))
                    print(f"Mean credit\t\t{(colored("N/A", "red") if len(credits) == 0 else colored(output.currency(float(np.mean(credits))), "green"))} (Std. dev. {np.std(credits) : .2f})")
                    print(f"Median credit\t\t{(colored("N/A", "red") if len(credits) == 0 else colored(output.currency(float(np.median(credits))), "green"))}")
                    print(f"Mean debit\t\t{colored(("N/A" if len(debits) == 0 else output.currency(float(np.mean(debits)))), "red")} (Std. dev. {np.std(debits) : .2f})")
                    print(f"Median debit\t\t{(colored("N/A", "red") if len(credits) == 0 else colored(output.currency(float(np.median(debits))), "red"))}")
                    print(f"Mean entry amount\t{colored("N/A" if len(amounts) == 0 else output.currency(float(np.mean(amounts))), ("green" if sum(amounts) > 0 else "red"))} (Std. dev. {np.std(amounts) : .2f})")
                    print(f"Median entry amount\t{colored("N/A" if len(amounts) == 0 else output.currency(float(np.median(amounts))), ("green" if np.median(amounts) > 0 else "red"))}")
                    print(f"Total credit\t\t{colored("N/A", "red") if len(credits) == 0 else colored(output.currency(sum(credits)), "green")}")
                    print(f"Total debit\t\t{colored("N/A", "red") if len(credits) == 0 else colored(output.currency(sum(debits)), "red")}")
                    print(colored(f"Grand total\t\t{colored("N/A", "red", attrs=["bold"]) if len(amounts) == 0 else colored(output.currency(sum(amounts)), ("green" if sum(amounts) > 0 else "red"), attrs=["bold"])}", attrs=["bold"]))


        case "category":
            if args.create:
                if len(args.create[1]) != 6:
                    output.error("Color must be in hex format (i.e. FFFFFF).")
                else:
                    parse_create(con, Category, args.create)

            if args.list:
                parse_list(con, Category)

            if args.delete:
                parse_delete(con, Category, args.delete)


        case "entry":
            if args.create:
                num = 0
                try:
                    num = float(args.create[1])
                except ValueError:
                    output.error("Amount must be a number.")
                except IndexError:
                    output.error("Expected 5 arguments (name, amount, category, account, date).")
                else:
                    if num == 0:
                        output.error("Cannot create an entry with a dollar value of 0.")
                    else:
                        acc_name = args.create[3]
                        cat_name = args.create[2]

                        cur.execute("SELECT * FROM accounts WHERE name = ?", (acc_name,))
                        res = cur.fetchall()

                        if len(res) == 0:
                            output.error(f"Unknown account \"{acc_name}\".")
                        else:
                            cur.execute("SELECT * FROM categories WHERE name = ?", (cat_name,))
                            res2 = cur.fetchall()

                            if len(res2) == 0:
                                output.error(f"Unknown category \"{cat_name}\".")
                            else:
                                is_duplicate = parse_create(con, Entry, args.create)
                                if not is_duplicate and not args.exempt:
                                    cur.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?", (num, acc_name))

                                    if num >= 0:
                                        output.success(f"Added {output.currency(num)} to account {acc_name}'s balance.")
                                    else:
                                        output.success(f"Subtracted {output.currency(num)[1:]} from account {acc_name}'s balance.")

                                    # if balance is less than 0
                                    new_balance = res[0][1] + num
                                    if new_balance < 0:
                                        output.warning(f"Account {acc_name}'s balance is less than 0 ({output.currency(new_balance)})!")

            if args.list:
                parse_list(con, Entry)

            if args.delete:
                parse_delete(con, Entry, args.delete)


        case _:
            output.error("Unknown component. Must be \"account\", \"category\", or \"entry\".")

    con.commit()
    con.close()

# ACADEMIC INTEGRITY STATEMENT
# I have not used source code obtained from any other unauthorized
# source, either modified or unmodified.  Neither have I provided
# access to my code to another. The project I am submitting
# is my own original work.
