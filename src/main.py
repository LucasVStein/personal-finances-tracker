from datetime import date

from internal_libs.category import Category
from internal_libs.expense import Expense

def main():
    e = Expense(date.today(), "Team dinner", Category.FOOD, 16.74)
    print(e)

if __name__ == "__main__":
    main()
