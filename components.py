import sqlite3 as sql
import datetime as dt

DB_NAME = "pyft.db"

class Category:
    name: str
    color: str

    def __init__(self, name: str, color: str):
        self.name = name
        self.color = color

    def update_db(self, connection: sql.Connection):
        cur = connection.cursor()
        cur.execute("""
            INSERT INTO categories VALUES (?, ?)
            ON CONFLICT (name)
            DO UPDATE SET name = excluded.?, color = excluded.?;
            """, self.name, self.color, self.name, self.color)

        connection.commit()



class Account:
    name: str
    balance: float

    def __init__(self, name: str):
        self.name = name
        self.balance = 0

    def update_db(self, connection: sql.Connection):
        cur = connection.cursor()
        cur.execute("""
            INSERT INTO accounts VALUES (?, ?)
            ON CONFLICT (name)
            DO UPDATE SET name = excluded.?, balance = excluded.?;
            """, self.name, self.balance, self.name, self.balance)

        connection.commit()



class Entry:
    name: str
    amount: float
    category: Category
    account: Account
    date: dt.date

    def __init__(self, name: str, amount: float, category: Category, account: Account, date: dt.date):
        self.name = name
        self.amount = amount
        self.category = category
        self.account = account
        self.date = date

    def update_db(self, connection: sql.Connection):
        cur = connection.cursor()
        cur.execute("""
            INSERT INTO accounts VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (name)
            DO UPDATE SET name = excluded.?, accountname = excluded.?, amount = excluded.?, date = excluded.?, category = excluded.?;
            """, self.name, self.account.name, self.amount, self.date.isoformat(), self.category.name, self.name, self.account.name, self.amount, self.date.isoformat(), self.category.name)

        connection.commit()



def init_db():
    con = sql.connect(DB_NAME)
    cur = con.cursor()

    cur.execute("""CREATE TABLE categories (
        name VARCHAR(255) PRIMARY KEY,
        color VARCHAR(6)
    )""")

    cur.execute("""CREATE TABLE entries (
        name VARCHAR(255) PRIMARY KEY,
        accountname VARCHAR(255),
        amount DECIMAL(11, 2),
        date DATE,
        category VARCHAR(255),
        FOREIGN KEY (accountname) REFERENCES accounts(name),
        FOREIGN KEY (category) REFERENCES categories(name)
    )""")

    cur.execute("""CREATE TABLE accounts (
        name VARCHAR(255) PRIMARY KEY,
        balance DECIMAL(11, 2)
    )""")

    con.commit()
    con.close()
