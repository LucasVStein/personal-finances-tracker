from datetime import date

from .category import Category

class Expense:
    def __init__(self, date: date, description: str, category: Category, amount: float):
        self._date = date
        self._description = description
        self._category = category
        self._amount = amount

    def __repr__(self):
        return f"Expense(date: {self._date}, description: \"{self._description}\", category: {self._category.value}, amount: {self._amount})"
