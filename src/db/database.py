import sqlite3
from pathlib import Path

from internal_libs.expense import Expense

SCHEMA_PATH = Path(__file__).parent / "schema.sql"
DB_DEFAULT_PATH = "finances.db"

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

def init_db(db_path: str = DB_DEFAULT_PATH):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    with open(SCHEMA_PATH) as inf:
        schema = inf.read()
    cursor.executescript(schema)

    connection.commit()
    connection.close()

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

def del_expense(id: int, db_path: str = DB_DEFAULT_PATH) -> bool:
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute(DB_DELETE_EXPENSE_COMMAND, (id,))
    connection.commit()
    connection.close()

    return cursor.rowcount > 0
