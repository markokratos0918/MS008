import datetime as dt
from .errors import ValidationError


def ensure_non_empty(*fields):
    for label, value in fields:
        if not value:
            raise ValidationError(f"{label} is required.")


def ensure_positive_int(label: str, value: int):
    if not isinstance(value, int) or value <= 0:
        raise ValidationError(f"{label} must be a positive integer.")


def ensure_non_negative(label: str, value):
    if value < 0:
        raise ValidationError(f"{label} must be non-negative.")


def validate_rental_window(start: dt.date, end: dt.date, min_days: int, max_days: int) -> int:
    if end <= start:
        raise ValidationError("End date must be after start date.")
    days = (end - start).days
    if not (min_days <= days <= max_days):
        raise ValidationError(f"Rental length must be between {min_days} and {max_days} days.")
    return days
