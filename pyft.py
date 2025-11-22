import argparse
from components import *
import output

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
        output.error("Unknown context. Must be \"account\", \"category\", or \"entry\"")
