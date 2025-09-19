from __future__ import annotations
from typing import Optional, Iterable
from del_tor_cars.models import User
from del_tor_cars.hashing import HashingFactory, HashingStrategy

class UserRepo:
    def __init__(self, db, hasher: HashingStrategy | None = None):
        self.db = db
        self.hasher = hasher or HashingFactory.get()

    def create_customer(self, first, last, email, phone, password):
        with self.db.connect() as conn:
            conn.execute(
                "INSERT INTO users(first_name,last_name,email,phone,password,role) VALUES(?,?,?,?,?,?)",
                (first, last, email, phone, self.hasher.hash(password), "customer"),
            )

    def add_user(self, first, last, email, phone, password, role):
        assert role in ("admin", "customer")
        with self.db.connect() as conn:
            conn.execute(
                "INSERT INTO users(first_name,last_name,email,phone,password,role) VALUES(?,?,?,?,?,?)",
                (first, last, email, phone, self.hasher.hash(password), role),
            )

    def login(self, email: str, password: str) -> Optional[User]:
        with self.db.connect() as conn:
            row = conn.execute(
                "SELECT id, first_name, role, password FROM users WHERE email=?", (email,)
            ).fetchone()
        if not row:
            return None
        if not self.hasher.verify(password, row["password"]):
            return None
        return User(row["id"], row["first_name"], row["role"])

    def list_users(self) -> Iterable:
        with self.db.connect() as conn:
            return list(conn.execute("SELECT id, first_name, last_name, email, role FROM users ORDER BY id"))

    def update_role(self, user_id: int, role: str) -> bool:
        with self.db.connect() as conn:
            return conn.execute("UPDATE users SET role=? WHERE id=?", (role, user_id)).rowcount > 0

    def delete(self, user_id: int) -> bool:
        with self.db.connect() as conn:
            return conn.execute("DELETE FROM users WHERE id=?", (user_id,)).rowcount > 0
