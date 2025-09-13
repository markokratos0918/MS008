class RentalRepo:
    def __init__(self, db):
        self.db = db

    def create(self, user_id, car_id, start, end, days, base, extras, total, status="pending") -> int:
        with self.db.connect() as conn:
            cur = conn.execute(
                "INSERT INTO rentals(user_id,car_id,start_date,end_date,days,base_total,extras_total,grand_total,status,created_at) "
                "VALUES(?,?,?,?,?,?,?,?,?,datetime('now'))",
                (user_id, car_id, start.isoformat(), end.isoformat(), days, base, extras, total, status),
            )
            return cur.lastrowid

    def list_for_user(self, user_id):
        with self.db.connect() as conn:
            return list(
                conn.execute(
                    "SELECT r.id, c.make||' '||c.model AS car, r.start_date, r.end_date, r.days, r.grand_total, r.status "
                    "FROM rentals r JOIN cars c ON c.id=r.car_id WHERE r.user_id=? ORDER BY r.id DESC",
                    (user_id,),
                )
            )

    def list_all(self):
        with self.db.connect() as conn:
            return list(
                conn.execute(
                    "SELECT r.id, u.first_name||' ('||u.email||')' AS customer, c.make||' '||c.model AS car, "
                    "r.start_date, r.end_date, r.days, r.grand_total, r.status "
                    "FROM rentals r JOIN users u ON u.id=r.user_id JOIN cars c ON c.id=r.car_id ORDER BY r.id DESC"
                )
            )

    def approve(self, rental_id: int) -> bool:
        with self.db.connect() as conn:
            row = conn.execute("SELECT car_id, status FROM rentals WHERE id=?", (rental_id,)).fetchone()
            if not row or row[1] != "pending":
                return False
            car_id = row[0]
            car = conn.execute("SELECT available_now FROM cars WHERE id=?", (car_id,)).fetchone()
            if not car or car[0] <= 0:
                return False
            conn.execute("UPDATE rentals SET status='approved' WHERE id=? AND status='pending'", (rental_id,))
            conn.execute("UPDATE cars SET available_now = available_now - 1 WHERE id=?", (car_id,))
            return True

    def reject(self, rental_id: int) -> bool:
        with self.db.connect() as conn:
            return conn.execute(
                "UPDATE rentals SET status='rejected' WHERE id=? AND status='pending'", (rental_id,)
            ).rowcount > 0

    def return_rental(self, rental_id: int, for_user_id=None) -> bool:
        with self.db.connect() as conn:
            row = conn.execute("SELECT id, car_id, status, user_id FROM rentals WHERE id=?", (rental_id,)).fetchone()
            if not row:
                return False
            if for_user_id is not None and row[3] != for_user_id:
                return False
            if row[2] != "approved":
                return False
            conn.execute("UPDATE rentals SET status='returned' WHERE id=?", (rental_id,))
            conn.execute("UPDATE cars SET available_now = available_now + 1 WHERE id=?", (row[1],))
            return True
