import sys
import os
import pytest
import argparse
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

import cli.cli as cli
from internal_libs.category import ExpCategory
from internal_libs.category import IncCategory
import db.database as db

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

def test_date_validation_positive():
    """test the date validation when a correct input is passed"""

    res = cli.validate_date("1998-06-04")
    
    assert res.year == 1998
    assert res.month == 6
    assert res.day == 4

def test_date_validation_negative():
    """test the date validation when an incorrect input is passed"""

    with pytest.raises(argparse.ArgumentTypeError) as err:
        cli.validate_date("wrong format")

    expected_out = "Invalid date format: \"wrong format\". Expected YYYY-MM-DD."
    assert str(err.value) == expected_out

def test_show_balance_positive(monkeypatch, capsys):
    """positive test the show balance function"""

    monkeypatch.setattr(db, "get_balance", lambda: (True, 1500))

    cli.handle_show_balance()
    out = capsys.readouterr().out
    expected_out = "Current balance: 1500.00€\n"

    assert out == expected_out

def test_show_balance_negative(monkeypatch, capsys):
    """negative test the show balance function"""

    monkeypatch.setattr(db, "get_balance", lambda: (False, "Database error"))

    cli.handle_show_balance()
    out = capsys.readouterr().out
    expected_out = "ERROR: Database error.\n"

    assert out == expected_out

def test_set_balance_positive(monkeypatch, capsys):
    """test the positive result of the set balance function"""

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
    """test the negative result of the set balance function"""

    monkeypatch.setattr(db, "set_balance", lambda balance: False)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.balance = 1000

    cli.handle_set_balance(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Error while trying to change the balance value.\n"

    assert out == expected_out

def test_list_expenses_handler_positive(monkeypatch, capsys):
    """positive test function that handles the list expenses command"""

    dummyExpenses = [(0, "1998-06-04", "description test", "gaming", 70),
                     (1, "2025-10-24", "description test 2", "other", 5)]
    monkeypatch.setattr(db, "get_expenses", lambda: (True, dummyExpenses))

    cli.handle_exp_list_command()
    out = capsys.readouterr().out
    expected_out = (
        "(id:0) Expense(date: 1998-06-04, description: \"description test\", category: Gaming, amount: 70.00€)\n"
        "(id:1) Expense(date: 2025-10-24, description: \"description test 2\", category: Other, amount: 5.00€)\n"
    )

    assert out == expected_out

def test_list_expenses_handler_negative(monkeypatch, capsys):
    """negative test function that handles the list expenses command"""

    monkeypatch.setattr(db, "get_expenses", lambda: (False, "Database error"))

    cli.handle_exp_list_command()
    out = capsys.readouterr().out
    expected_out = "ERROR: Database error.\n"

    assert out == expected_out

def test_add_expense_positive_1(monkeypatch, capsys):
    """test the positive result of adding a new expense with custom values"""

    monkeypatch.setattr(db, "add_expense", lambda expense: True)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = 20
    dummy.date = date.fromisoformat("2025-09-05")
    dummy.description = "test description"
    dummy.category = ExpCategory.TRANSPORT

    cli.handle_add_exp_command(dummy)
    out = capsys.readouterr().out
    expected_out = "SUCCESS: Expense added to the db.\n"

    assert out == expected_out

def test_add_expense_positive_2(monkeypatch, capsys):
    """test the positive result of adding a new expense with default values"""

    monkeypatch.setattr(db, "add_expense", lambda expense: True)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = 15
    dummy.date = None
    dummy.description = None
    dummy.category = None

    cli.handle_add_exp_command(dummy)
    out = capsys.readouterr().out
    expected_out = "SUCCESS: Expense added to the db.\n"

    assert out == expected_out

def test_add_expense_negative_1(capsys):
    """test the negative result of adding a new expense with a negative amount"""

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = -5
    dummy.date = None
    dummy.description = None
    dummy.category = None

    cli.handle_add_exp_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Amount needs to be positive (> 0).\n"

    assert out == expected_out

def test_add_expense_negative_2(monkeypatch, capsys):
    """test the negative result of adding a new expense with a db error"""

    monkeypatch.setattr(db, "add_expense", lambda expense: False)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = 50
    dummy.date = None
    dummy.description = None
    dummy.category = None

    cli.handle_add_exp_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Error while trying to add Expense to db.\n"

    assert out == expected_out

def test_edit_expense_positive(monkeypatch, capsys):
    """test the positive result of editing an expense"""

    monkeypatch.setattr(db, "edit_expense", lambda *expense: True)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = 20
    dummy.date = None
    dummy.description = "test desc"
    dummy.category = None
    dummy.id = 1

    cli.handle_edit_exp_command(dummy)
    out = capsys.readouterr().out
    expected_out = "SUCCESS: Edit successful.\n"

    assert out == expected_out

def test_edit_expense_negative_1(capsys):
    """test the negative result of editing an expense with no data selected"""

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = None
    dummy.date = None
    dummy.description = None
    dummy.category = None

    cli.handle_edit_exp_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Choose at least one expense data to edit.\n"

    assert out == expected_out

def test_edit_expense_negative_2(capsys):
    """test the negative result of editing an expense with a negative amount"""

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = -10
    dummy.date = None
    dummy.description = None
    dummy.category = None

    cli.handle_edit_exp_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Amount needs to be positive (> 0).\n"

    assert out == expected_out

def test_edit_expense_negative_3(monkeypatch, capsys):
    """test the negative result of editing an expense with a db error"""

    monkeypatch.setattr(db, "edit_expense", lambda *expense: False)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = 2
    dummy.date = None
    dummy.description = "test"
    dummy.category = None
    dummy.id = 1

    cli.handle_edit_exp_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Edit failed.\n"

    assert out == expected_out

def test_delete_expense_positive(monkeypatch, capsys):
    """test the positive result of deleting an expense"""

    monkeypatch.setattr(db, "del_expense", lambda id: True)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.id = 1

    cli.handle_del_exp_command(dummy)
    out = capsys.readouterr().out
    expected_out = "SUCCESS: Deletion successful.\n"

    assert out == expected_out

def test_delete_expense_negative(monkeypatch, capsys):
    """test the negative result of deleting an expense with a db error"""

    monkeypatch.setattr(db, "del_expense", lambda id: False)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.id = 1

    cli.handle_del_exp_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Deletion failed.\n"

    assert out == expected_out

def test_exp_category_validation_positive():
    """test the expense category validation when a correct input is passed"""

    res = cli.validate_expense_category("food")

    assert type(res) == ExpCategory
    assert res.value == ExpCategory.FOOD.value
    assert res.name == ExpCategory.FOOD.name

def test_exp_category_validation_negative():
    """test the expense category validation when an incorrect input is passed"""

    with pytest.raises(argparse.ArgumentTypeError) as err:
        cli.validate_expense_category("wrong format")

    expected_out = f"Invalid category: \"wrong format\". Choose from {[category.value for category in ExpCategory]}."
    assert str(err.value) == expected_out

def test_list_incomes_handler_positive(monkeypatch, capsys):
    """positive test function that handles the list incomes command"""

    dummyIncomes = [(0, "2025-10-27", "description test", "salary", 2000),
                    (1, "2025-10-24", "description test 2", "other", 5)]
    monkeypatch.setattr(db, "get_incomes", lambda: (True, dummyIncomes))

    cli.handle_inc_list_command()
    out = capsys.readouterr().out
    expected_out = (
        "(id:0) Income(date: 2025-10-27, description: \"description test\", category: Salary, amount: 2000.00€)\n"
        "(id:1) Income(date: 2025-10-24, description: \"description test 2\", category: Other, amount: 5.00€)\n"
    )

    assert out == expected_out

def test_list_incomes_handler_negative(monkeypatch, capsys):
    """negative test function that handles the list incomes command"""

    monkeypatch.setattr(db, "get_incomes", lambda: (False, "Database error"))

    cli.handle_inc_list_command()
    out = capsys.readouterr().out
    expected_out = "ERROR: Database error.\n"

    assert out == expected_out

def test_add_income_positive_1(monkeypatch, capsys):
    """test the positive result of adding a new income with custom values"""

    monkeypatch.setattr(db, "add_income", lambda income: True)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = 20
    dummy.date = date.fromisoformat("2025-09-05")
    dummy.description = "test description"
    dummy.category = IncCategory.INVESTMENT

    cli.handle_add_inc_command(dummy)
    out = capsys.readouterr().out
    expected_out = "SUCCESS: Income added to the db.\n"

    assert out == expected_out

def test_add_income_positive_2(monkeypatch, capsys):
    """test the positive result of adding a new income with default values"""

    monkeypatch.setattr(db, "add_income", lambda income: True)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = 15
    dummy.date = None
    dummy.description = None
    dummy.category = None

    cli.handle_add_inc_command(dummy)
    out = capsys.readouterr().out
    expected_out = "SUCCESS: Income added to the db.\n"

    assert out == expected_out

def test_add_income_negative_1(capsys):
    """test the negative result of adding a new income with a negative amount"""

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = -5
    dummy.date = None
    dummy.description = None
    dummy.category = None

    cli.handle_add_inc_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Amount needs to be positive (> 0).\n"

    assert out == expected_out

def test_add_income_negative_2(monkeypatch, capsys):
    """test the negative result of adding a new income with a db error"""

    monkeypatch.setattr(db, "add_income", lambda income: False)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = 50
    dummy.date = None
    dummy.description = None
    dummy.category = None

    cli.handle_add_inc_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Error while trying to add Income to db.\n"

    assert out == expected_out

def test_edit_income_positive(monkeypatch, capsys):
    """test the positive result of editing an income"""

    monkeypatch.setattr(db, "edit_income", lambda *income: True)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = 20
    dummy.date = None
    dummy.description = "test desc"
    dummy.category = None
    dummy.id = 1

    cli.handle_edit_inc_command(dummy)
    out = capsys.readouterr().out
    expected_out = "SUCCESS: Edit successful.\n"

    assert out == expected_out

def test_edit_income_negative_1(capsys):
    """test the negative result of editing an income with no data selected"""

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = None
    dummy.date = None
    dummy.description = None
    dummy.category = None

    cli.handle_edit_inc_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Choose at least one income data to edit.\n"

    assert out == expected_out

def test_edit_income_negative_2(capsys):
    """test the negative result of editing an income with a negative amount"""

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = -10
    dummy.date = None
    dummy.description = None
    dummy.category = None

    cli.handle_edit_inc_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Amount needs to be positive (> 0).\n"

    assert out == expected_out

def test_edit_income_negative_3(monkeypatch, capsys):
    """test the negative result of editing an income with a db error"""

    monkeypatch.setattr(db, "edit_income", lambda *income: False)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.amount = 2
    dummy.date = None
    dummy.description = "test"
    dummy.category = None
    dummy.id = 1

    cli.handle_edit_inc_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Edit failed.\n"

    assert out == expected_out

def test_delete_income_positive(monkeypatch, capsys):
    """test the positive result of deleting an income"""

    monkeypatch.setattr(db, "del_income", lambda id: True)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.id = 1

    cli.handle_del_inc_command(dummy)
    out = capsys.readouterr().out
    expected_out = "SUCCESS: Deletion successful.\n"

    assert out == expected_out

def test_delete_income_negative(monkeypatch, capsys):
    """test the negative result of deleting an income with a db error"""

    monkeypatch.setattr(db, "del_income", lambda id: False)

    class DummyClass:
        pass
    dummy = DummyClass()
    dummy.id = 1

    cli.handle_del_inc_command(dummy)
    out = capsys.readouterr().out
    expected_out = "ERROR: Deletion failed.\n"

    assert out == expected_out

def test_inc_category_validation_positive():
    """test the income category validation when a correct input is passed"""

    res = cli.validate_income_category("salary")

    assert type(res) == IncCategory
    assert res.value == IncCategory.SALARY.value
    assert res.name == IncCategory.SALARY.name

def test_inc_category_validation_negative():
    """test the income category validation when an incorrect input is passed"""

    with pytest.raises(argparse.ArgumentTypeError) as err:
        cli.validate_income_category("wrong format")

    expected_out = f"Invalid category: \"wrong format\". Choose from {[category.value for category in IncCategory]}."
    assert str(err.value) == expected_out

@pytest.mark.parametrize("argv, handler_name", [
    (["src/main.py", "show_balance"], "handle_show_balance"),
    (["src/main.py", "set_balance", "1000"], "handle_set_balance"),
    (["src/main.py", "list_exp"], "handle_exp_list_command"),
    (["src/main.py", "list_inc"], "handle_inc_list_command"),
    (["src/main.py", "categories"], "handle_categories_command"),
    (["src/main.py", "add_exp", "10"], "handle_add_exp_command"),
    (["src/main.py", "edit_exp", "1", "--amount", "10"], "handle_edit_exp_command"),
    (["src/main.py", "del_exp", "1"], "handle_del_exp_command"),
    (["src/main.py", "add_inc", "2000"], "handle_add_inc_command"),
    (["src/main.py", "edit_inc", "1", "--amount", "10"], "handle_edit_inc_command"),
    (["src/main.py", "del_inc", "1"], "handle_del_inc_command"),
])
def test_cli_dispatch(monkeypatch, argv, handler_name):
    """test the main function of cli, to see if the correct handler is called depending on each command"""
    
    result = {"called": False}
    def set_flag(*args):
        result["called"] = True

    monkeypatch.setattr(sys, "argv", argv)
    monkeypatch.setattr(cli, handler_name, set_flag)

    cli.main()

    assert result["called"]
    