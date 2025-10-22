import sys
import os
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from internal_libs.expense import Expense
from internal_libs.category import ExpCategory

def test_expense_default_values():
    """testing if the default values for the Expense class are correctly assigned"""
    
    e = Expense(10)

    assert e.amount == 10 # only non-default value

    assert e.date == date.today()
    assert e.description == ""
    assert e.category == ExpCategory.OTHER

def test_expense_construction():
    """testing the expense constructor correctly initializes the values"""
    
    e = Expense(50, date(1998, 6, 4), "test description", ExpCategory.GAMING)

    assert e.amount == 50
    assert e.date == date(1998, 6, 4)
    assert e.description == "test description"
    assert e.category == ExpCategory.GAMING

def test_expense_repr():
    """testing the __repr__ method"""

    e = Expense(50, date(1998, 6, 4), "test description", ExpCategory.GAMING)
    assert e.__repr__() == "Expense(date: 1998-06-04, description: \"test description\", category: Gaming, amount: 50.00€)"

def test_expense_categories():
    """testing the list_categories method"""

    assert ExpCategory.list() == Expense.list_categories()
