from datetime import date

from .category import Category

class Expense:
    def __init__(self, amount: float, date: date = date.today(), description: str = "", category: Category = Category.OTHER):
        self.amount = amount
        self.date = date
        self.description = description
        self.category = category

    def __repr__(self):
        return f"Expense(date: {self.date}, description: \"{self.description}\", category: {self.category.value}, amount: {self.amount}€)"

    @classmethod
    def list_categories(cls):
        return Category.list()
