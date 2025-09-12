from datetime import date

import db.database as db
from internal_libs.category import Category
from internal_libs.expense import Expense

def main():
    e = Expense(date.today(), "Team dinner", Category.FOOD, 16.74)
    print(e)
    print("---------------------------")

    db.init_db()
    db.add_expense(e)
    db.get_expenses()

if __name__ == "__main__":
    main()
