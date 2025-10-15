import sqlite3
from pathlib import Path

from internal_libs.expense import Expense
from internal_libs.income import Income

SCHEMA_PATH = Path(__file__).parent / "schema.sql"
DB_DEFAULT_PATH = "finances.db"

DB_GET_BALANCE_COMMAND = """
    SELECT * FROM balance
"""

DB_SET_BALANCE_COMMAND = """
    UPDATE balance SET curr_balance = ? WHERE id = 1
"""

def init_db(db_path: str = DB_DEFAULT_PATH):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    with open(SCHEMA_PATH) as inf:
        schema = inf.read()
    cursor.executescript(schema)

    # check if balance already exists, if not initialize it to 0
    cursor.execute("SELECT COUNT(*) FROM balance")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO balance (id, curr_balance) VALUES (1, 0)")

    connection.commit()
    connection.close()

def get_balance(db_path: str = DB_DEFAULT_PATH):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(DB_GET_BALANCE_COMMAND)
    balance = cursor.fetchone()[1] # index 0 is id, index 1 is balance
    connection.close()
    
    return balance

def set_balance(balance: int, db_path: str = DB_DEFAULT_PATH) -> bool:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(DB_SET_BALANCE_COMMAND, (balance,))
    connection.commit()
    connection.close()

    return cursor.rowcount == 1

# EXPENSES DB LOGIC _______________________________________________

DB_GETALL_EXPENSES_COMMAND = """
    SELECT * FROM expenses
"""

DB_INSERT_EXPENSE_COMMAND = """
    INSERT INTO expenses (date, description, category, amount)
    VALUES (? ,? ,?, ?)
"""

DB_DELETE_EXPENSE_COMMAND = """
    DELETE FROM expenses WHERE id = ?
"""

def get_expenses(db_path: str = DB_DEFAULT_PATH):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(DB_GETALL_EXPENSES_COMMAND)
    expenses = cursor.fetchall()
    connection.close()
    
    return expenses

def add_expense(expense: Expense, db_path: str = DB_DEFAULT_PATH):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(DB_INSERT_EXPENSE_COMMAND, (expense.date.isoformat(),
                                               expense.description,
                                               expense.category.name,
                                               expense.amount))
    
    connection.commit()
    connection.close()

def edit_expense(id: int, new_date = None, new_description = None, new_category = None, new_amount = None, db_path: str = DB_DEFAULT_PATH) -> bool:
    fields = []
    values = []

    if new_date is not None:
        fields.append("date = ?")
        values.append(new_date)
    if new_description is not None:
        fields.append("description = ?")
        values.append(new_description)
    if new_category is not None:
        fields.append("category = ?")
        values.append(new_category)
    if new_amount is not None:
        fields.append("amount = ?")
        values.append(new_amount)

    if not fields or not values:
        return False # should never happen
    
    values.append(id)

    query_str = f"UPDATE expenses SET {", ".join(fields)} WHERE id = ?"

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query_str, tuple(values))
    connection.commit()
    connection.close()

    return cursor.rowcount > 0

def del_expense(id: int, db_path: str = DB_DEFAULT_PATH) -> bool:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(DB_DELETE_EXPENSE_COMMAND, (id,))
    connection.commit()
    connection.close()

    return cursor.rowcount > 0

# INCOMES DB LOGIC _______________________________________________

DB_GETALL_INCOMES_COMMAND = """
    SELECT * FROM incomes
"""

DB_INSERT_INCOME_COMMAND = """
    INSERT INTO incomes (date, description, category, amount)
    VALUES (? ,? ,?, ?)
"""

DB_DELETE_INCOME_COMMAND = """
    DELETE FROM incomes WHERE id = ?
"""

def get_incomes(db_path: str = DB_DEFAULT_PATH):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(DB_GETALL_INCOMES_COMMAND)
    incomes = cursor.fetchall()
    connection.close()
    
    return incomes

def add_income(income: Income, db_path: str = DB_DEFAULT_PATH):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(DB_INSERT_INCOME_COMMAND, (income.date.isoformat(),
                                              income.description,
                                              income.category.name,
                                              income.amount))
    
    connection.commit()
    connection.close()

def edit_income(id: int, new_date = None, new_description = None, new_category = None, new_amount = None, db_path: str = DB_DEFAULT_PATH) -> bool:
    fields = []
    values = []

    if new_date is not None:
        fields.append("date = ?")
        values.append(new_date)
    if new_description is not None:
        fields.append("description = ?")
        values.append(new_description)
    if new_category is not None:
        fields.append("category = ?")
        values.append(new_category)
    if new_amount is not None:
        fields.append("amount = ?")
        values.append(new_amount)

    if not fields or not values:
        return False # should never happen
    
    values.append(id)

    query_str = f"UPDATE incomes SET {", ".join(fields)} WHERE id = ?"

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query_str, tuple(values))
    connection.commit()
    connection.close()

    return cursor.rowcount > 0

def del_income(id: int, db_path: str = DB_DEFAULT_PATH) -> bool:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(DB_DELETE_INCOME_COMMAND, (id,))
    connection.commit()
    connection.close()

    return cursor.rowcount > 0
