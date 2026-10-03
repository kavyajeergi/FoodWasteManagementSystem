from dataclasses import dataclass
from datetime import date


@dataclass
class FoodItem:
    id: str
    name: str
    category: str
    quantity: float
    unit: str
    purchase_date: date
    expiry_date: date
