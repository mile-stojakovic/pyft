import argparse
from components import *

parser = argparse.ArgumentParser()

parser.add_argument("context", help="The context in which to operate (account, category, or entry)")

args = parser.parse_args()

match args.context:
    case "account":
        print("Account settings")
    case "category":
        print("Category settings")
    case "entry":
        print("Entry settings")
    case _:
        print("error: unknown context. Must be \"account\", \"category\", or \"entry\"")
