from datetime import datetime


def validate_datetime(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return ValueError("Incorrect date format, should be YYYY-MM-DD")


def validate_quantity(quantity):
    if quantity <= 0:
        raise ValueError("Quantity cannot be negative")
    return quantity


def validate_expiry_date(purchase_date, expiry_date):
    if expiry_date <= purchase_date:
        raise ValueError("Expiry date must be after purchase date")
