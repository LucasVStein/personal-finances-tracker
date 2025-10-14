from datetime import date

from .category import IncCategory

class Income:
    def __init__(self, amount: float, date: date = date.today(), description: str = "", category: IncCategory = IncCategory.OTHER):
        self.amount = amount
        self.date = date
        self.description = description
        self.category = category

    def __repr__(self):
        return f"Income(date: {self.date}, description: \"{self.description}\", category: {self.category.value}, amount: {self.amount:.2f}€)"

    @classmethod
    def list_categories(cls):
        return IncCategory.list()
