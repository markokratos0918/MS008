from __future__ import annotations
import sqlite3
from .config import DB_NAME, SEED_ON_BOOT
from .utils import hash_password


class Database:
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name
        self._init_db()
        if SEED_ON_BOOT:
            self._seed()

    def connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _init_db(self) -> None:
        with self.connect() as conn:
            cur = conn.cursor()
            # Users
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name  TEXT NOT NULL,
                    email      TEXT NOT NULL UNIQUE,
                    phone      TEXT NOT NULL,
                    password   TEXT NOT NULL,
                    role       TEXT NOT NULL CHECK (role IN ('admin','customer'))
                );
                """
            )
            # Cars
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS cars (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    make        TEXT NOT NULL,
                    model       TEXT NOT NULL,
                    color       TEXT NOT NULL,
                    year        INTEGER NOT NULL CHECK (year >= 1886),
                    mileage     INTEGER NOT NULL CHECK (mileage >= 0) DEFAULT 0,
                    daily_rate  REAL    NOT NULL CHECK (daily_rate >= 0),
                    available_now INTEGER NOT NULL CHECK (available_now >= 0) DEFAULT 0,
                    min_days    INTEGER NOT NULL CHECK (min_days >= 1) DEFAULT 1,
                    max_days    INTEGER NOT NULL CHECK (max_days >= 1) DEFAULT 30,
                    UNIQUE(make, model, year, color)
                );
                """
            )
            # Rentals
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS rentals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    car_id  INTEGER NOT NULL,
                    start_date TEXT NOT NULL,  -- YYYY-MM-DD
                    end_date   TEXT NOT NULL,  -- YYYY-MM-DD
                    days       INTEGER NOT NULL CHECK (days > 0),
                    base_total REAL NOT NULL CHECK (base_total >= 0),
                    extras_total REAL NOT NULL CHECK (extras_total >= 0),
                    grand_total REAL NOT NULL CHECK (grand_total >= 0),
                    status TEXT NOT NULL CHECK (status IN ('pending','approved','rejected','returned')),
                    created_at TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY(car_id)  REFERENCES cars(id)  ON DELETE CASCADE
                );
                """
            )

    def _seed(self) -> None:
        with self.connect() as conn:
            cur = conn.cursor()
            # Users
            cur.execute("SELECT COUNT(*) FROM users")
            if cur.fetchone()[0] == 0:
                cur.executemany(
                    """
                    INSERT INTO users(first_name,last_name,email,phone,password,role)
                    VALUES(?,?,?,?,?,?)
                    """,
                    [
                        ("Admin", "One", "admin@example.com", "0000", hash_password("0000"), "admin"),
                        ("Alice", "Customer", "alice@example.com", "1111", hash_password("1111"), "customer"),
                    ],
                )
            # Cars
            cur.execute("SELECT COUNT(*) FROM cars")
            if cur.fetchone()[0] == 0:
                cur.executemany(
                    """
                    INSERT INTO cars(make,model,color,year,mileage,daily_rate,available_now,min_days,max_days)
                    VALUES(?,?,?,?,?,?,?,?,?)
                    """,
                    [
                        ("Toyota", "Corolla", "White", 2020, 34000, 75.0, 2, 1, 21),
                        ("Honda", "Civic", "Black", 2021, 22000, 85.0, 1, 1, 30),
                        ("Tesla", "Model 3", "Blue", 2022, 12000, 140.0, 1, 2, 30),
                    ],
                )
