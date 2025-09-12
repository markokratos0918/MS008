from typing import Optional, Iterable
from ..models import User
from ..utils import hash_password

class UserRepo:
    def __init__(self, db):
        self.db = db

    def create_customer(self, first, last, email, phone, password):
        with self.db.connect() as conn:
            conn.execute(
                "INSERT INTO users(first_name,last_name,email,phone,password,role) VALUES(?,?,?,?,?,?)",
                (first, last, email, phone, hash_password(password), "customer"),
            )
    def add_user(self, first, last, email, phone, password, role):
        assert role in ("admin", "customer")
        with self.db.connect() as conn:
            conn.execute(
                "INSERT INTO users(first_name,last_name,email,phone,password,role) VALUES(?,?,?,?,?,?)",
                (first, last, email, phone, hash_password(password), role),
            )
    def login(self, email: str, password: str) -> Optional[User]:
        with self.db.connect() as conn:
            cur = conn.execute(
                "SELECT id, first_name, role FROM users WHERE email=? AND password=?",
                (email, hash_password(password)),
            )
            row = cur.fetchone()
            return User(row[0], row[1], row[2]) if row else None
    def list_users(self) -> Iterable:
        with self.db.connect() as conn:
            return list(conn.execute("SELECT id, first_name, last_name, email, role FROM users ORDER BY id"))

    def update_role(self, user_id: int, role: str) -> bool:
        with self.db.connect() as conn:
            return conn.execute("UPDATE users SET role=? WHERE id=?", (role, user_id)).rowcount > 0

    def delete(self, user_id: int) -> bool:
        with self.db.connect() as conn:
            return conn.execute("DELETE FROM users WHERE id=?", (user_id,)).rowcount > 0