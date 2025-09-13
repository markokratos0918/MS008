from ..repos import UserRepo, CarRepo, RentalRepo
from ..validators import ensure_non_empty, ensure_non_negative, ensure_positive_int
from ..errors import ValidationError


class AdminService:
    def __init__(self, users: UserRepo, cars: CarRepo, rentals: RentalRepo):
        self.users, self.cars, self.rentals = users, cars, rentals

    def add_car(self, make, model, color, year, mileage, rate, stock, min_days, max_days) -> bool:
        ensure_non_empty(("Make", make), ("Model", model), ("Color", color))
        ensure_positive_int("Year", int(year))
        ensure_non_negative("Mileage", int(mileage))
        ensure_non_negative("Daily rate", float(rate))
        ensure_non_negative("Stock", int(stock))
        ensure_positive_int("Min days", int(min_days))
        ensure_positive_int("Max days", int(max_days))
        if max_days < min_days:
            raise ValidationError("Max days must be >= Min days.")
        self.cars.add(
            make, model, color, int(year), int(mileage), float(rate), int(stock), int(min_days), int(max_days)
        )
        return True

    def approve(self, rental_id: int) -> bool:
        return self.rentals.approve(rental_id)

    def reject(self, rental_id: int) -> bool:
        return self.rentals.reject(rental_id)
