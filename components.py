import sqlite3 as sql
import datetime as dt
import output

DB_NAME = "pyft.db"

class PYFTComponent:
    format_name = "component"
    name: str

    def __init__(self, name: str):
        self.name = name

    def update_db(self, connection: sql.Connection) -> bool:
        return False



class Category(PYFTComponent):
    format_name = "category"
    color: str

    def __init__(self, name: str, color: str):
        super().__init__(name)
        self.color = color

    def update_db(self, connection: sql.Connection) -> bool:
        out = False
        cur = connection.cursor()
        cur.execute("SELECT * FROM categories WHERE name = ?", (self.name,))
        res = cur.fetchall()
        if len(res) == 0:
            cur.execute("INSERT INTO categories VALUES (?, ?)", (self.name, self.color,))
        else:
            output.warning(f"Already found category with name \"{self.name}\". Updating...")
            cur.execute("UPDATE categories SET name = ?, color = ? WHERE name = ?", (self.name, self.color, self.name,))
            out = True

        connection.commit()
        return out




class Account(PYFTComponent):
    format_name = "account"
    balance: float

    def __init__(self, name: str, balance: float = 0):
        super().__init__(name)
        self.balance = balance

    def update_db(self, connection: sql.Connection) -> bool:
        out = False
        cur = connection.cursor()
        cur.execute("SELECT * FROM accounts WHERE name = ?", (self.name,))
        res = cur.fetchall()
        if len(res) == 0:
            cur.execute("INSERT INTO accounts VALUES (?, ?)", (self.name, self.balance,))
        else:
            output.warning(f"Already found account with name \"{self.name}\". Updating...")
            cur.execute("UPDATE accounts SET name = ?, balance = ? WHERE name = ?", (self.name, self.balance, self.name,))
            out = True

        connection.commit()
        return out



class Entry(PYFTComponent):
    format_name = "entry"
    amount: float
    category_name: str
    account_name: str
    date: dt.date

    def __init__(self, name: str, amount: float, category_name: str, account_name: str, date: str):
        super().__init__(name)
        self.amount = amount
        self.category_name = category_name
        self.account_name = account_name
        self.date = output.str_to_date(date)

    def update_db(self, connection: sql.Connection) -> bool:
        out = False
        cur = connection.cursor()
        cur.execute("SELECT * FROM entries WHERE name = ?", (self.name,))
        res = cur.fetchall()
        if len(res) == 0:
            cur.execute("INSERT INTO entries VALUES (?, ?, ?, ?, ?)", (self.name, self.account_name, self.amount, self.date.isoformat(), self.category_name,))
        else:
            output.warning(f"Already found entry with name \"{self.name}\". Account {self.account_name}'s balance will not be changed. Updating...")
            cur.execute("UPDATE entries SET name = ?, amount = ?, category = ?, accountname = ?, date = ? WHERE name = ?", (self.name, self.amount, self.category_name, self.account_name, self.date.isoformat(), self.name,))
            out = True

        connection.commit()
        return out


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
