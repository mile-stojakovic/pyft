import json
import datetime as dt

class Category:
    name: str
    color: str

    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

class Entry:
    name: str
    amount: float
    category: Category
    date: dt.date

    def __init__(self, name: str, amount: float, category: Category, date: dt.date):
        self.name = name
        self.amount = amount
        self.category = category
        self.date = date

class Account:
    name: str
    balance: float
    entries: list[Entry]
    categories: list[Category]

    def __init__(self, name: str):
        self.name = name
        self.balance = 0
        self.entries = []
        self.categories = [Category("Uncategorized", "gray")]

def pyftJSONSerializer(object):
    if isinstance(object, Category):
        return object.name
    elif isinstance(object, dt.date):
        return object.isoformat()
    return object.__dict__
