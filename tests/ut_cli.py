import sys
import os
import pytest
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

import cli.cli as cli
from internal_libs.category import ExpCategory
from internal_libs.category import IncCategory
import db.database as db
from internal_libs.expense import Expense
from internal_libs.income import Income

def test_show_categories(capsys):
    """test if the categories are correctly listed"""

    cli.handle_categories_command()
    out = capsys.readouterr().out
    expected_out = f"Possible categories for Expenses: {ExpCategory.list()}\nPossible categories for Incomes: {IncCategory.list()}\n"
    expected_out = (
        f"Possible categories for Expenses: {ExpCategory.list()}\n"
        f"Possible categories for Incomes: {IncCategory.list()}\n"
    )

    assert out == expected_out

def test_date_validation_correct_input():
    """test the date validation when a correct input is passed"""

    res = cli.validate_date("1998-06-04")
    
    assert res.year == 1998
    assert res.month == 6
    assert res.day == 4

def test_date_validation_incorrect_input():
    """test the date validation when an incorrect input is passed"""

    with pytest.raises(argparse.ArgumentTypeError) as err:
        cli.validate_date("wrong format")

    expected_out = "Invalid date format: \"wrong format\". Expected YYYY-MM-DD."
    assert str(err.value) == expected_out

def test_show_balance(monkeypatch, capsys):
    """test the show balance method"""

    monkeypatch.setattr(db, "get_balance", lambda: 1500)

    cli.handle_show_balance()
    out = capsys.readouterr().out
    expected_out = "Current balance: 1500.00€\n"

    assert out == expected_out

def test_set_balance_positive(monkeypatch, capsys):
    """test the positive result of the set balance method"""

    monkeypatch.setattr(db, "set_balance", lambda balance: True)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.balance = 1000

    cli.handle_set_balance(dummy)
    out = capsys.readouterr().out
    expected_out = "SUCCESS: New balance set.\n"

    assert out == expected_out

def test_set_balance_negative(monkeypatch, capsys):
    """test the negative result of the set balance method"""

    monkeypatch.setattr(db, "set_balance", lambda balance: False)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.balance = 1000

    cli.handle_set_balance(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Not possible to update balance.\n"

    assert out == expected_out

def test_list_expenses_handler(monkeypatch, capsys):
    """test method that handles the list expenses command"""

    dummyExpenses = [(0, "1998-06-04", "description test", "gaming", 70),
                     (1, "2025-10-24", "description test 2", "other", 5)]
    monkeypatch.setattr(db, "get_expenses", lambda: dummyExpenses)

    cli.handle_exp_list_command()
    out = capsys.readouterr().out
    expected_out = (
        "(id:0) Expense(date: 1998-06-04, description: \"description test\", category: Gaming, amount: 70.00€)\n"
        "(id:1) Expense(date: 2025-10-24, description: \"description test 2\", category: Other, amount: 5.00€)\n"
    )

    assert out == expected_out
