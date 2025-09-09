import sqlite3
import datetime
import hashlib

DB_NAME =  "carrental.db"

def _hash_password(password):
    return hashlib.sha256(pw.encode("utf-8")).hexdigest() # Simple SHA-256 hash

class Database:

    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.init_db
        self.import_sample_data()

    def connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    
    def init_db(self):
        conn = self.connect()
        cur = conn.cursor()

        cur.executeC(
            """
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Brand TEXT NOT NULL,
                Model TEXT NOT NULL,
                Color TEXT NOT NULL,
                Year  INTEGER NOT NULL CHECK (Year >= 1886),
                Price  REAL NOT NULL CHECK (Price >= 0),   -- per hour
                Available INTEGER NOT NULL CHECK (Available >= 0)
            )
            """
        )

        # Composite uniqueness for car identity
        cur.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS idx_cars_brand_model_year_color
            ON cars(Brand, Model, Year, Color
            )
            """
        )

        conn.commit()
        conn.close()

    def import_sample_data(self):
        """Seed data if tables are empty."""
        conn = self.connect()
        cur = conn.cursor()

        # Users
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchone()[0] == 0:
            users = [
                ('Admin',  'One',  'admin@example.com',  '0000',     _hash_password('0000'), 1),
                ('Admin',  'Two',  'admin2@example.com', '222222',   _hash_password('1234'), 1),
                ('Client', 'User', 'client@example.com', '111111',   _hash_password('1111'), 0),
            ]
            cur.executemany("""
                INSERT INTO users(FirstName, LastName, Email, PhoneNumber, Password, Type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, users)

        # Cars
        cur.execute("SELECT COUNT(*) FROM cars")
        if cur.fetchone()[0] == 0:
            cars = [
                ('Toyota', 'Corolla', 'White', 2020, 1000.0, 2),
                ('Honda',  'Civic',   'Black', 2021, 1200.0, 1),
            ]
            cur.executemany("""
                INSERT INTO cars(Brand, Model, Color, Year, Price, Available)
                VALUES (?, ?, ?, ?, ?, ?)
            """, cars)

        conn.commit()
        conn.close()