import argparse
from datetime import datetime

from internal_libs.category import ExpCategory
from internal_libs.category import IncCategory
from internal_libs.expense import Expense
from internal_libs.income import Income
import db.database as db

def handle_categories_command(args):
    print(f"Possible categories for Expenses: {Expense.list_categories()}")
    print(f"Possible categories for Incomes: {Income.list_categories()}")

def validate_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: \"{date}\". Expected YYYY-MM-DD.")

# EXPENSES CLI LOGIC _______________________________________________

def handle_exp_list_command(args):
    for exp in db.get_expenses():
        id = exp[0]
        exp_class = Expense(exp[4],                           # exp[4] = amount
                            exp[1],                           # exp[1] = date
                            exp[2],                           # exp[2] = description
                            ExpCategory(exp[3].capitalize())) # exp[3] = category
        print(f"(id:{id}) {exp_class}")

def handle_add_exp_command(args):
    expense = Expense(args.amount,
                      args.date if args.date else datetime.today().date(),
                      args.description if args.description else "",
                      args.category if args.category else ExpCategory.OTHER)
    db.add_expense(expense)

def handle_edit_exp_command(args):
    if args.date is None and args.description is None and args.category is None and args.amount is None:
        print("ERROR: Choose at least one expense data to edit.")
        return
    print("SUCCESS: Edit successful" if db.edit_expense(args.id, args.date, args.description, args.category, args.amount)
          else "ERROR: Edit failed.")

def handle_del_exp_command(args):
    print("SUCCESS: Deletion successful" if db.del_expense(args.id) else "ERROR: Deletion failed.")
    
def validate_expense_category(category: str):
    if category.capitalize() not in [category.value for category in ExpCategory]:
        raise argparse.ArgumentTypeError(f"Invalid category: \"{category}\". Choose from {[category.value for category in ExpCategory]}.")
    return ExpCategory(category.capitalize())

# INCOMES CLI LOGIC ________________________________________________

def handle_inc_list_command(args):
    for inc in db.get_incomes():
        id = inc[0]
        inc_class = Income(inc[4],                           # inc[4] = amount
                           inc[1],                           # inc[1] = date
                           inc[2],                           # inc[2] = description
                           IncCategory(inc[3].capitalize())) # inc[3] = category
        print(f"(id:{id}) {inc_class}")

def handle_add_inc_command(args):
    income = Income(args.amount,
                    args.date if args.date else datetime.today().date(),
                    args.description if args.description else "",
                    args.category if args.category else IncCategory.OTHER)
    db.add_income(income)

def handle_edit_inc_command(args):
    if args.date is None and args.description is None and args.category is None and args.amount is None:
        print("ERROR: Choose at least one income data to edit.")
        return
    print("SUCCESS: Edit successful" if db.edit_income(args.id, args.date, args.description, args.category, args.amount)
          else "ERROR: Edit failed.")

def handle_del_inc_command(args):
    print("SUCCESS: Deletion successful" if db.del_income(args.id) else "ERROR: Deletion failed.")

def validate_income_category(category: str):
    if category.capitalize() not in [category.value for category in IncCategory]:
        raise argparse.ArgumentTypeError(f"Invalid category: \"{category}\". Choose from {[category.value for category in IncCategory]}.")
    return IncCategory(category.capitalize())

# __________________________________________________________________

def main():
    parser = argparse.ArgumentParser(description = "Personal Finances Tracker CLI")
    subparsers = parser.add_subparsers(dest = "command", required = True)

    exp_list_parser = subparsers.add_parser("list_exp", help = "Lists all expenses")
    inc_list_parser = subparsers.add_parser("list_inc", help = "Lists all incomes")

    category_parser = subparsers.add_parser("categories", help = "Lists all expense and income categories")

    add_exp_parser = subparsers.add_parser("add_exp", help = "Adds a new expense")
    add_exp_parser.add_argument("amount", type = float, help = "Amount of the expense")
    add_exp_parser.add_argument("--description", help = "Description of the expense", metavar = "")
    add_exp_parser.add_argument("--date", type = validate_date, help = "Date of the expense (YYYY-MM-DD)", metavar = "")
    add_exp_parser.add_argument("--category", type = validate_expense_category, help = "Category of the expense", metavar = "")

    add_inc_parser = subparsers.add_parser("add_inc", help = "Adds a new income")
    add_inc_parser.add_argument("amount", type = float, help = "Amount of the income")
    add_inc_parser.add_argument("--description", help = "Description of the income", metavar = "")
    add_inc_parser.add_argument("--date", type = validate_date, help = "Date of the income (YYYY-MM-DD)", metavar = "")
    add_inc_parser.add_argument("--category", type = validate_income_category, help = "Category of the income", metavar = "")

    edit_exp_parser = subparsers.add_parser("edit_exp", help = "Edit a expense")
    edit_exp_parser.add_argument("id", type = int, help = "ID of the expense")
    edit_exp_parser.add_argument("--amount", type = float, help = "New amount of the expense")
    edit_exp_parser.add_argument("--description", help = "New description of the expense", metavar = "")
    edit_exp_parser.add_argument("--date", type = validate_date, help = "New date of the expense (YYYY-MM-DD)", metavar = "")
    edit_exp_parser.add_argument("--category", type = validate_expense_category, help = "New category of the expense", metavar = "")

    edit_inc_parser = subparsers.add_parser("edit_inc", help = "Edit a income")
    edit_inc_parser.add_argument("id", type = int, help = "ID of the income")
    edit_inc_parser.add_argument("--amount", type = float, help = "New amount of the income")
    edit_inc_parser.add_argument("--description", help = "New description of the income", metavar = "")
    edit_inc_parser.add_argument("--date", type = validate_date, help = "New date of the income (YYYY-MM-DD)", metavar = "")
    edit_inc_parser.add_argument("--category", type = validate_income_category, help = "New category of the income", metavar = "")

    del_exp_parser = subparsers.add_parser("del_exp", help = "Deletes the expense")
    del_exp_parser.add_argument("id", type = int, help = "ID of the expense")

    del_inc_parser = subparsers.add_parser("del_inc", help = "Deletes the income")
    del_inc_parser.add_argument("id", type = int, help = "ID of the income")

    args = parser.parse_args()
    if args.command == "list_exp":
        handle_exp_list_command(args)
    elif args.command == "categories":
        handle_categories_command(args)
    elif args.command == "add_exp":
        handle_add_exp_command(args)
    elif args.command == "edit_exp":
        handle_edit_exp_command(args)
    elif args.command == "del_exp":
        handle_del_exp_command(args)
    elif args.command == "list_inc":
        handle_inc_list_command(args)
    elif args.command == "add_inc":
        handle_add_inc_command(args)
    elif args.command == "edit_inc":
        handle_edit_inc_command(args)
    elif args.command == "del_inc":
        handle_del_inc_command(args)
    else:
        print("ERROR: Unknown command.") # should never happen

if __name__ == "__main__":
    main()
