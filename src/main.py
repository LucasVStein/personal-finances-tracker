from datetime import date

import db.database as db
from internal_libs.category import Category
from internal_libs.expense import Expense

def main():
    e1 = Expense(date.today(), "Tiago Anniversary", Category.FOOD, 16.74)
    e2 = Expense(date.today(), "Borderlands 4", Category.GAMING, 69.99)
    e3 = Expense(date.today(), "Diesel", Category.TRANSPORT, 50)

    db.init_db()
    db.add_expense(e1)
    db.add_expense(e2)
    db.add_expense(e3)

    db.get_expenses()

if __name__ == "__main__":
    main()
