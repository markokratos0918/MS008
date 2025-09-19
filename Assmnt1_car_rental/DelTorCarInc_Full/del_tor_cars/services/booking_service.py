# del_tor_cars/services/booking_service.py
from __future__ import annotations
from del_tor_cars.repos.rental_repo import RentalRepo
from del_tor_cars.errors import NotFoundError
from del_tor_cars.validators import validate_rental_window
from del_tor_cars.pricing import PricingStrategy, PricingFactory


class BookingService:
    def __init__(self, db, rentals: RentalRepo, pricing: PricingStrategy | None = None):
        self.db = db
        self.rentals = rentals
        # allow DI from the factory; default to standard pricing
        self.pricing = pricing or PricingFactory.get("standard")

    def create_booking(self, user_id: int, car_id: int, start, end, extras: float = 0.0) -> int:
        # read car policy (rate, min/max days)
        with self.db.connect() as conn:
            car = conn.execute(
                "SELECT daily_rate, min_days, max_days FROM cars WHERE id=?", (car_id,)
            ).fetchone()
        if not car:
            raise NotFoundError("Car not found.")

        days = validate_rental_window(start, end, car[1], car[2])

        # use injected pricing strategy
        base, extras_total, total = self.pricing.calc(days, float(car[0]), extras)

        return self.rentals.create(
            user_id, car_id, start, end, days, base, extras_total, total, status="pending"
        )
