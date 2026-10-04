from dataclasses import dataclass
from datetime import date
from enum import Enum


@dataclass
class FoodItem:
    id: str
    name: str
    category: str
    quantity: float
    unit: str
    purchase_date: date
    expiry_date: date


@dataclass
class ItemAction:
    item_name: str
    action: ActionStatus
    action_date: date
