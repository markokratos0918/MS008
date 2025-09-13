from ..repos import RentalRepo
from ..errors import NotFoundError
from ..validators import validate_rental_window
from ..services.fee_calculator import FeeCalculator


class BookingService:
    def __init__(self, db, rentals: RentalRepo):
        self.db, self.rentals = db, rentals

    def create_booking(self, user_id: int, car_id: int, start, end, extras: float = 0.0) -> int:
        with self.db.connect() as conn:
            car = conn.execute(
                "SELECT daily_rate, min_days, max_days FROM cars WHERE id=?",
                (car_id,),
            ).fetchone()
        if not car:
            raise NotFoundError("Car not found.")
        days = validate_rental_window(start, end, car[1], car[2])
        base, extras_total, total = FeeCalculator.calc(days, float(car[0]), extras)
        return self.rentals.create(
            user_id, car_id, start, end, days, base, extras_total, total, status="pending"
        )