import sqlite3
import pytest
from datetime import date

import db.database as db
from internal_libs.expense import Expense, ExpCategory
from internal_libs.income import Income, IncCategory

@pytest.fixture
def tmp_db(tmp_path):
    """create a temporary db for testing"""

    db_path = tmp_path / "test_finances.db"
    success = db.init_db(db_path)

    assert success, "Failed to initialize test database"

    return db_path

def test_init_db_creates_balance_table(tmp_db):
    """test if calling init_db creates the balance table 0 initialized"""

    connection = sqlite3.connect(tmp_db)
    cursor = connection.cursor()

    cursor.execute("SELECT curr_balance FROM balance")
    balance = cursor.fetchone()[0]

    connection.close()

    assert balance == 0

def test_init_db_negative_1(monkeypatch):
    """test if init_db returns False when a database error is raised"""

    def mock_connect(_):
        raise sqlite3.Error("connection failed")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    assert not db.init_db("fake_path")

def test_init_db_negative_2(monkeypatch):
    """test if init_db returns False when a generic error is raised"""

    def mock_connect(_):
        raise RuntimeError("generic error")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    assert not db.init_db("fake_path")

def test_get_balance(tmp_db):
    """test the get_balance db function"""

    success, balance = db.get_balance(tmp_db)

    assert success
    assert balance == 0

def test_get_balance_negative_1(monkeypatch):
    """test if get_balance returns False when a database error is raised"""

    def mock_connect(_):
        raise sqlite3.Error("connection failed")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    success, message = db.get_balance("fake_path")

    assert not success
    assert message == "Database error"

def test_get_balance_negative_2(monkeypatch):
    """test if get_balance returns False when a generic error is raised"""

    def mock_connect(_):
        raise RuntimeError("generic error")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    success, message = db.get_balance("fake_path")

    assert not success
    assert message == "Unexpected error"

def test_set_balance(tmp_db):
    """test the set_balance db function"""

    success, balance = db.get_balance(tmp_db)

    assert success
    assert balance == 0

    success = db.set_balance(1000, tmp_db)

    assert success

    success, balance = db.get_balance(tmp_db)

    assert success
    assert balance == 1000

def test_set_balance_negative_1(monkeypatch):
    """test if set_balance returns False when a database error is raised"""

    def mock_connect(_):
        raise sqlite3.Error("connection failed")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    assert not db.set_balance("fake_path")

def test_set_balance_negative_2(monkeypatch):
    """test if set_balance returns False when a generic error is raised"""

    def mock_connect(_):
        raise RuntimeError("generic error")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    assert not db.set_balance("fake_path")

def test_get_add_expenses(tmp_db):
    """test the db get_expenses and add_expense functions"""

    expense1 = Expense(50)
    expense2 = Expense(2, date(2024, 4, 1), "test description", ExpCategory.FOOD)

    success1 = db.add_expense(expense1, tmp_db)
    success2 = db.add_expense(expense2, tmp_db)

    assert success1
    assert success2

    success, expenses = db.get_expenses(tmp_db)

    assert success
    assert len(expenses) == 2
    assert expenses[1][3] == ExpCategory.FOOD.name # 1 to get the second expense, 3 is the positional value of .category

def test_get_expenses_negative_1(monkeypatch):
    """test if get_expenses returns False when a database error is raised"""

    def mock_connect(_):
        raise sqlite3.Error("connection failed")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    success, msg = db.get_expenses("fake_path")

    assert not success
    assert msg == "Database error"

def test_get_expenses_negative_2(monkeypatch):
    """test if get_expenses returns False when a generic error is raised"""

    def mock_connect(_):
        raise RuntimeError("generic error")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    success, msg = db.get_expenses("fake_path")

    assert not success
    assert msg == "Unexpected error"

def test_add_expense_negative_1(monkeypatch):
    """test if add_expense returns False when a database error is raised"""

    def mock_connect(_):
        raise sqlite3.Error("connection failed")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    assert not db.add_expense(Expense(0), "fake_path")

def test_add_expense_negative_2(monkeypatch):
    """test if add_expense returns False when a generic error is raised"""

    def mock_connect(_):
        raise RuntimeError("generic error")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    assert not db.add_expense(Expense(0), "fake_path")

def test_edit_expense(tmp_db):
    """test the db edit_expenses function"""

    db.add_expense(Expense(50), tmp_db)
    success1 = db.edit_expense(1, new_amount = 1000, new_category = "Utilities", new_date = date(2020, 1, 2), new_description = "description", db_path = tmp_db)
    success2, expenses = db.get_expenses(tmp_db)

    assert success1
    assert success2
    assert expenses[0][0] == 1
    assert expenses[0][1] == "2020-01-02"
    assert expenses[0][2] == "description"
    assert expenses[0][3] == ExpCategory.UTILITIES.value
    assert expenses[0][4] == 1000

def test_edit_expense_negative_1(monkeypatch):
    """test if edit_expense returns False when a database error is raised"""

    def mock_connect(_):
        raise sqlite3.Error("connection failed")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    assert not db.edit_expense(1, new_amount = 10, db_path = "fake_path")

def test_edit_expense_negative_2(monkeypatch):
    """test if edit_expense returns False when a generic error is raised"""

    def mock_connect(_):
        raise RuntimeError("generic error")
    monkeypatch.setattr(sqlite3, "connect", mock_connect)

    assert not db.edit_expense(1, new_amount = 10, db_path = "fake_path")

def test_edit_expense_negative_3(tmp_db):
    """test if edit_expense returns False when a no values are passed"""

    assert not db.edit_expense(1, db_path = tmp_db)
