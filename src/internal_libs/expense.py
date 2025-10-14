from datetime import date

from .category import ExpCategory

class Expense:
    def __init__(self, amount: float, date: date = date.today(), description: str = "", category: ExpCategory = ExpCategory.OTHER):
        self.amount = amount
        self.date = date
        self.description = description
        self.category = category

    def __repr__(self):
        return f"Expense(date: {self.date}, description: \"{self.description}\", category: {self.category.value}, amount: {self.amount:.2f}€)"

    @classmethod
    def list_categories(cls):
        return ExpCategory.list()
