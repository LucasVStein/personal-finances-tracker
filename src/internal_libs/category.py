from enum import Enum

class ExpCategory(Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    GAMING = "Gaming"
    UTILITIES = "Utilities"
    OTHER = "Other"

    @classmethod
    def list(cls):
        return [c.value for c in cls]

class IncCategory(Enum):
    SALARY = "Salary"
    INVESTMENT = "Investment"
    OTHER = "Other"

    @classmethod
    def list(cls):
        return [c.value for c in cls]
