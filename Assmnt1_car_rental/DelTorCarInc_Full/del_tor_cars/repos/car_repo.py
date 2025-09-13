from ..models import Car


class CarRepo:
    def __init__(self, db):
        self.db = db

    def all(self):
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT id, make, model, color, year, mileage, daily_rate, available_now, min_days, max_days "
                "FROM cars ORDER BY make, model, year"
            ).fetchall()
            return [Car(*row) for row in rows]

    def available(self):
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT id, make, model, color, year, mileage, daily_rate, available_now, min_days, max_days "
                "FROM cars WHERE available_now > 0 ORDER BY make, model, year"
            ).fetchall()
            return [Car(*row) for row in rows]

    def add(self, make, model, color, year, mileage, daily_rate, available_now, min_days, max_days):
        with self.db.connect() as conn:
            conn.execute(
                "INSERT INTO cars(make,model,color,year,mileage,daily_rate,available_now,min_days,max_days) "
                "VALUES(?,?,?,?,?,?,?,?,?)",
                (make, model, color, year, mileage, daily_rate, available_now, min_days, max_days),
            )

    def update_field(self, car_id: int, field: str, value) -> bool:
        allowed = {"make", "model", "color", "year", "mileage", "daily_rate", "available_now", "min_days", "max_days"}
        if field not in allowed:
            return False
        with self.db.connect() as conn:
            return conn.execute(f"UPDATE cars SET {field}=? WHERE id=?", (value, car_id)).rowcount > 0

    def delete(self, car_id: int) -> bool:
        with self.db.connect() as conn:
            return conn.execute("DELETE FROM cars WHERE id=?", (car_id,)).rowcount > 0