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

def init_db(db_path: str = DB_DEFAULT_PATH) -> bool:
    try:
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

        return True
    
    except sqlite3.Error as e:
        return False
    
    except Exception as e:
        return False

def get_balance(db_path: str = DB_DEFAULT_PATH) -> tuple[bool, float | str]:
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(DB_GET_BALANCE_COMMAND)
        balance = cursor.fetchone()[1] # index 0 is id, index 1 is balance
        connection.close()
        
        return True, balance
    
    except sqlite3.Error as e:
        return False, "Database error"
    
    except Exception as e:
        return False, "Unexpected error"

def set_balance(balance: int, db_path: str = DB_DEFAULT_PATH) -> bool:
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(DB_SET_BALANCE_COMMAND, (balance,))
        connection.commit()
        connection.close()

        return cursor.rowcount == 1
    
    except sqlite3.Error as e:
        return False
    
    except Exception as e:
        return False

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

def get_expenses(db_path: str = DB_DEFAULT_PATH) -> tuple[bool, list | str]:
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(DB_GETALL_EXPENSES_COMMAND)
        expenses = cursor.fetchall()
        connection.close()
        
        return True, expenses
    
    except sqlite3.Error as e:
        return False, "Database error"
    
    except Exception as e:
        return False, "Unexpected error"

def add_expense(expense: Expense, db_path: str = DB_DEFAULT_PATH) -> bool:
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(DB_INSERT_EXPENSE_COMMAND, (expense.date.isoformat(),
                                                expense.description,
                                                expense.category.name,
                                                expense.amount))
        
        cursor.execute(DB_GET_BALANCE_COMMAND)
        new_balance = cursor.fetchone()[1] - expense.amount
        cursor.execute(DB_SET_BALANCE_COMMAND, (new_balance,))
        
        connection.commit()
        connection.close()

        return True

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

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

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        if new_amount is not None:
            cursor.execute("SELECT * FROM expenses WHERE id = ?", (id,))
            old_amount = cursor.fetchone()[4] # 4 is the position of the amount
            diff = old_amount - new_amount

            cursor.execute("UPDATE balance SET curr_balance = curr_balance + ? WHERE id = 1", (diff,))

        cursor.execute(query_str, tuple(values))

        connection.commit()
        connection.close()

        return cursor.rowcount > 0
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def del_expense(id: int, db_path: str = DB_DEFAULT_PATH) -> bool:
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM expenses WHERE id = ?", (id,))
        diff = cursor.fetchone()[4]
        cursor.execute("UPDATE balance SET curr_balance = curr_balance + ? WHERE id = 1", (diff,))

        cursor.execute(DB_DELETE_EXPENSE_COMMAND, (id,))
        connection.commit()
        connection.close()

        return cursor.rowcount > 0
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

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

def get_incomes(db_path: str = DB_DEFAULT_PATH) -> tuple[bool, list | str]:
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(DB_GETALL_INCOMES_COMMAND)
        incomes = cursor.fetchall()
        connection.close()
        
        return True, incomes
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False, f"Database error: {e}"
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False, f"Unexpected error: {e}"

def add_income(income: Income, db_path: str = DB_DEFAULT_PATH) -> bool:
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute(DB_INSERT_INCOME_COMMAND, (income.date.isoformat(),
                                                income.description,
                                                income.category.name,
                                                income.amount))
        
        cursor.execute(DB_GET_BALANCE_COMMAND)
        new_balance = cursor.fetchone()[1] + income.amount
        cursor.execute(DB_SET_BALANCE_COMMAND, (new_balance,))
        
        connection.commit()
        connection.close()

        return True

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

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

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        if new_amount is not None:
            cursor.execute("SELECT * FROM incomes WHERE id = ?", (id,))
            old_amount = cursor.fetchone()[4] # 4 is the position of the amount
            diff = old_amount - new_amount

            cursor.execute("UPDATE balance SET curr_balance = curr_balance - ? WHERE id = 1", (diff,))

        cursor.execute(query_str, tuple(values))
        connection.commit()
        connection.close()

        return cursor.rowcount > 0

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def del_income(id: int, db_path: str = DB_DEFAULT_PATH) -> bool:
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM incomes WHERE id = ?", (id,))
        diff = cursor.fetchone()[4]
        cursor.execute("UPDATE balance SET curr_balance = curr_balance - ? WHERE id = 1", (diff,))

        cursor.execute(DB_DELETE_INCOME_COMMAND, (id,))
        connection.commit()
        connection.close()

        return cursor.rowcount > 0
    
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
