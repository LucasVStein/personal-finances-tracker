from enum import Enum

class Category(Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    GAMING = "Gaming"
    UTILITIES = "Utilities"
    OTHER = "Other"

    @classmethod
    def list(cls):
        return [c.value for c in cls]
