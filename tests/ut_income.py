import sys
import os
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from internal_libs.income import Income
from internal_libs.category import IncCategory

def test_income_default_values():
    """testing if the default values for the Income class are correctly assigned"""
    
    i = Income(10)

    assert i.amount == 10 # only non-default value

    assert i.date == date.today()
    assert i.description == ""
    assert i.category == IncCategory.OTHER

def test_income_construction():
    """testing the income constructor correctly initializes the values"""
    
    i = Income(1500, date(2023, 10, 24), "test description", IncCategory.SALARY)

    assert i.amount == 1500
    assert i.date == date(2023, 10, 24)
    assert i.description == "test description"
    assert i.category == IncCategory.SALARY

def test_income_repr():
    """testing the __repr__ method"""

    i = Income(1500, date(2023, 10, 24), "test description", IncCategory.SALARY)
    assert i.__repr__() == "Income(date: 2023-10-24, description: \"test description\", category: Salary, amount: 1500.00€)"

def test_income_categories():
    """testing the list_categories method"""

    assert IncCategory.list() == Income.list_categories()
