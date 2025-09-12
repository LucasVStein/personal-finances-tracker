from datetime import date

from .category import Category

class Expense:
    def __init__(self, date: date, description: str, category: Category, amount: float):
        self.date = date
        self.description = description
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f"Expense(date: {self.date}, description: \"{self.description}\", category: {self.category.value}, amount: {self.amount})"
