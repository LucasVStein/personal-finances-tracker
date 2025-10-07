import argparse
from datetime import datetime

from internal_libs.category import Category
from internal_libs.expense import Expense
import db.database as db

def handle_list_command(args):
    for exp in db.get_expenses():
        id = exp[0]
        exp_class = Expense(exp[4],                        # exp[4] = amount
                            exp[1],                        # exp[1] = date
                            exp[2],                        # exp[2] = description
                            Category(exp[3].capitalize())) # exp[3] = category
        print(f"(id:{id}) {exp_class}")

def handle_categories_command(args):
    print(Expense.list_categories())

def handle_add_command(args):
    expense = Expense(args.amount,
                      args.date if args.date else datetime.today().date(),
                      args.description if args.description else "",
                      args.category if args.category else Category.OTHER)
    db.add_expense(expense)

def handle_edit_command(args):
    if args.date is None and args.description is None and args.category is None and args.amount is None:
        print("ERROR: Choose at least one expense data to edit.")
        return
    print("SUCCESS: Edit successful" if db.edit_expense(args.id, args.date, args.description, args.category, args.amount)
          else "ERROR: Edit failed.")

def handle_del_command(args):
    print("SUCCESS: Deletion successful" if db.del_expense(args.id) else "ERROR: Deletion failed.")

def validate_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: \"{date}\". Expected YYYY-MM-DD.")
    
def validate_category(category: str):
    if category.capitalize() not in [category.value for category in Category]:
        raise argparse.ArgumentTypeError(f"Invalid category: \"{category}\". Choose from {[category.value for category in Category]}.")
    return Category(category.capitalize())

def main():
    parser = argparse.ArgumentParser(description = "Personal Finances Tracker CLI")
    subparsers = parser.add_subparsers(dest = "command", required = True)

    list_parser = subparsers.add_parser("list", help = "Lists all expenses")

    category_parser = subparsers.add_parser("categories", help = "Lists all expense categories")

    add_parser = subparsers.add_parser("add", help = "Adds a new expense")
    add_parser.add_argument("amount", type = float, help = "Amount of the expense")
    add_parser.add_argument("--description", help = "Description of the expense", metavar = "")
    add_parser.add_argument("--date", type = validate_date, help = "Date of the expense (YYYY-MM-DD)", metavar = "")
    add_parser.add_argument("--category", type = validate_category, help = "Category of the expense", metavar = "")

    edit_parser = subparsers.add_parser("edit", help = "Edit a expense")
    edit_parser.add_argument("id", type = int, help = "ID of the expense")
    edit_parser.add_argument("--amount", type = float, help = "New amount of the expense")
    edit_parser.add_argument("--description", help = "New description of the expense", metavar = "")
    edit_parser.add_argument("--date", type = validate_date, help = "New date of the expense (YYYY-MM-DD)", metavar = "")
    edit_parser.add_argument("--category", type = validate_category, help = "New category of the expense", metavar = "")

    del_parser = subparsers.add_parser("del", help = "Deletes the expense")
    del_parser.add_argument("id", type = int, help = "ID of the expense")

    args = parser.parse_args()
    if args.command == "list":
        handle_list_command(args)
    elif args.command == "categories":
        handle_categories_command(args)
    elif args.command == "add":
        handle_add_command(args)
    elif args.command == "edit":
        handle_edit_command(args)
    elif args.command == "del":
        handle_del_command(args)
    else:
        print("ERROR: Unknown command.") # should never happen

if __name__ == "__main__":
    main()
