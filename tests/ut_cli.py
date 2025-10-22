import sys
import os
import pytest
import argparse
from datetime import date

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

import cli.cli as cli
from internal_libs.category import ExpCategory
from internal_libs.category import IncCategory

def test_show_categories(capsys):
    """test if the categories are correctly listed"""

    cli.handle_categories_command()
    out = capsys.readouterr().out
    expected_out = f"Possible categories for Expenses: {ExpCategory.list()}\nPossible categories for Incomes: {IncCategory.list()}\n"
    
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
