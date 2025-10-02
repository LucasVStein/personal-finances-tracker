import argparse
from datetime import datetime

from internal_libs.category import Category
from internal_libs.expense import Expense

def handle_list_command(args):
    print(f"this is list command with args: {args}")

def handle_categories_command(args):
    print(Expense.list_categories())

def handle_add_command(args):
    print(f"this is add command with args: {args}")

def validate_date(date):
    try:
        return datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: \"{date}\". Expected YYYY-MM-DD.")
    
def validate_category(category: str):
    if category.capitalize() not in [category.value for category in Category]:
        raise argparse.ArgumentTypeError(f"Invalid category: \"{category}\". Choose from {[category.value for category in Category]}.")
    return category.capitalize()

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

    args = parser.parse_args()
    if args.command == "list":
        handle_list_command(args)
    elif args.command == "categories":
        handle_categories_command(args)
    elif args.command == "add":
        handle_add_command(args)
    else:
        print("Unknown command.") # should never happen

if __name__ == "__main__":
    main()
