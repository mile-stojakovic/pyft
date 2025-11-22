from enum import Enum

class Category:
    name: str
    color: str

class Entry:
    name: str
    amount: float
    category: Category

class Account:
    name: str
    balance: float
    entries: list[Entry]
