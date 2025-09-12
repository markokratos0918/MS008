import sqlite3
import datetime
import hashlib


DB_NAME = "carrentalsystem.db"


def _hash_password(pw: str) -> str:
    # Simple SHA-256 hash (use bcrypt/argon2 in production)
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()


class Database:
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name
        self.init_db()
        self.import_sample_data()

    def connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def init_db(self):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Brand     TEXT NOT NULL,
            Model     TEXT NOT NULL,
            Color     TEXT NOT NULL,
            Year      INTEGER NOT NULL CHECK (Year >= 1886),
            Price     REAL NOT NULL CHECK (Price >= 0),   -- per hour
            Available INTEGER NOT NULL CHECK (Available >= 0)
        )
        """)

        # Composite uniqueness for car identity
        cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_cars_brand_model_year_color
        ON cars(Brand, Model, Year, Color)
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName   TEXT NOT NULL,
            LastName    TEXT NOT NULL,
            Email       TEXT NOT NULL UNIQUE,
            PhoneNumber TEXT NOT NULL,
            Password    TEXT NOT NULL,  -- hashed
            Type        INTEGER NOT NULL CHECK (Type IN (0,1))  -- 1=admin, 0=client
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS rents (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            User     INTEGER NOT NULL,
            Car      INTEGER NOT NULL,
            DateTime TEXT NOT NULL,     -- ISO 8601
            Hours    INTEGER NOT NULL CHECK (Hours > 0),
            Total    REAL NOT NULL CHECK (Total >= 0),
            Status   INTEGER NOT NULL CHECK (Status IN (0,1,2)), -- 0=pending,1=confirmed,2=returned/cancelled
            FOREIGN KEY(User) REFERENCES users(ID) ON DELETE CASCADE,
            FOREIGN KEY(Car)  REFERENCES cars(ID)  ON DELETE CASCADE
        )
        """)

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


class User:
    def __init__(self, user_id, first_name, user_type):
        self.id = user_id
        self.first_name = first_name
        self.type = user_type

    def is_admin(self):
        return self.type == 1


class CarRentalSystem:
    ADMIN_EDITABLE_USER_FIELDS = {"FirstName", "LastName", "Email", "PhoneNumber", "Password", "Type"}
    ADMIN_EDITABLE_CAR_FIELDS = {"Brand", "Model", "Color", "Year", "Price", "Available"}

    def __init__(self):
        self.db = Database()
        self.current_user = None

    # -------------------- AUTH --------------------
    def register(self):
        print("\n=== Register New Client ===")
        fname = input("First Name: ").strip()
        lname = input("Last Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone Number: ").strip()
        password = input("Password: ").strip()

        if not (fname and lname and email and phone and password):
            print("All fields are required.")
            return False

        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE Email=?", (email,))
        if cur.fetchone():
            print("Email already exists! Try logging in.")
            conn.close()
            return False

        cur.execute("""
            INSERT INTO users(FirstName, LastName, Email, PhoneNumber, Password, Type)
            VALUES (?, ?, ?, ?, ?, 0)
        """, (fname, lname, email, phone, _hash_password(password)))
        conn.commit()
        conn.close()

        print("Registration successful! You can now log in.")
        return True

    def login(self):
        print("\n=== Login ===")
        email = input("Email: ").strip()
        password = input("Password: ").strip()

        conn = self.db.connect()
        cur = conn.cursor()

        # 1) Try modern (hashed) login
        cur.execute(
            "SELECT ID, FirstName, Type FROM users WHERE Email=? AND Password=?",
            (email, _hash_password(password))
        )
        row = cur.fetchone()
        if row:
            conn.close()
            self.current_user = User(row["ID"], row["FirstName"], row["Type"])
            print(f"Welcome {self.current_user.first_name}!")
            return True

        # 2) Legacy fallback: plaintext comparison (old DBs), then auto-upgrade
        cur.execute("SELECT ID, FirstName, Type, Password FROM users WHERE Email=?", (email,))
        row = cur.fetchone()
        if row and row["Password"] == password:
            cur.execute("UPDATE users SET Password=? WHERE ID=?", (_hash_password(password), row["ID"]))
            conn.commit()
            conn.close()
            self.current_user = User(row["ID"], row["FirstName"], row["Type"])
            print(f"Welcome {self.current_user.first_name}! (Your password was upgraded securely.)")
            return True

        conn.close()
        print("Invalid login.")
        return False

    # -------------------- CLIENT --------------------
    def view_cars(self):
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("SELECT ID, Brand, Model, Color, Year, Price, Available FROM cars ORDER BY Brand, Model, Year")
        cars = cur.fetchall()
        conn.close()

        print("\nCars:")
        for c in cars:
            print(f"[{c['ID']}] {c['Brand']} {c['Model']} ({c['Color']}, {c['Year']}) - "
                  f"${c['Price']}/hour - {c['Available']} available")

    def rent_car(self):
        if not self.current_user or self.current_user.is_admin():
            print("Only logged-in clients can rent cars.")
            return

        self.view_cars()

        try:
            car_id = int(input("Enter Car ID to rent: ").strip())
            hours = int(input("Enter number of hours: ").strip())
            if hours <= 0:
                print("Hours must be a positive integer.")
                return
        except ValueError:
            print("Invalid input.")
            return

        conn = self.db.connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT Price, Available FROM cars WHERE ID=?", (car_id,))
            car = cur.fetchone()

            if not car:
                print("Car not found.")
                return
            if car["Available"] <= 0:
                print("Car not available.")
                return

            total = float(car["Price"]) * hours
            now_iso = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Transactional update
            cur.execute("""
                INSERT INTO rents(User, Car, DateTime, Hours, Total, Status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.current_user.id, car_id, now_iso, hours, total, 1))
            cur.execute("UPDATE cars SET Available = Available - 1 WHERE ID=? AND Available > 0", (car_id,))

            if cur.rowcount == 0:
                conn.rollback()
                print("Car just went out of stock. Try another car.")
                return

            conn.commit()
            print(f"Car rented successfully! Total: ${total:.2f}")
        finally:
            conn.close()

    def view_rents(self, all_users=False):
        conn = self.db.connect()
        cur = conn.cursor()
        if all_users:
            cur.execute("""
                SELECT r.ID, u.FirstName || ' ' || u.LastName AS Client,
                       c.Brand || ' ' || c.Model AS Car,
                       r.DateTime, r.Hours, r.Total, r.Status
                FROM rents r
                JOIN users u ON u.ID = r.User
                JOIN cars  c ON c.ID = r.Car
                ORDER BY r.DateTime DESC
            """)
        else:
            if not self.current_user:
                print("You need to log in first.")
                conn.close()
                return
            cur.execute("""
                SELECT r.ID, c.Brand || ' ' || c.Model AS Car,
                       r.DateTime, r.Hours, r.Total, r.Status
                FROM rents r
                JOIN cars c ON c.ID = r.Car
                WHERE r.User=?
                ORDER BY r.DateTime DESC
            """, (self.current_user.id,))
        rents = cur.fetchall()
        conn.close()

        print("\nRents:")
        status_map = {0: "Pending", 1: "Confirmed", 2: "Returned/Cancelled"}
        for r in rents:
            if all_users:
                print(f"[{r['ID']}] {r['Client']} | {r['Car']} | {r['DateTime']} | "
                      f"{r['Hours']}h | ${r['Total']:.2f} | {status_map.get(r['Status'], r['Status'])}")
            else:
                print(f"[{r['ID']}] {r['Car']} | {r['DateTime']} | {r['Hours']}h | "
                      f"${r['Total']:.2f} | {status_map.get(r['Status'], r['Status'])}")

    # ----- Return / Undo rental helpers -----
    def _undo_rent_transactional(self, rent_id: int) -> bool:
        """
        Returns True if a confirmed rental was set to returned/cancelled (Status 2)
        and the car's Available was incremented. False if no change.
        """
        conn = self.db.connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT ID, Car, Status FROM rents WHERE ID=?", (rent_id,))
            r = cur.fetchone()
            if not r:
                print("Rental not found.")
                return False

            if r["Status"] != 1:
                print("Rental is not in a confirmable state (already returned/cancelled or pending).")
                return False

            car_id = r["Car"]

            # Flip to Status=2 (returned/cancelled)
            cur.execute("UPDATE rents SET Status=2 WHERE ID=? AND Status=1", (rent_id,))
            if cur.rowcount == 0:
                print("Rental status changed by another process.")
                conn.rollback()
                return False

            # Restock
            cur.execute("UPDATE cars SET Available = Available + 1 WHERE ID=?", (car_id,))
            if cur.rowcount == 0:
                print("Failed to restock car.")
                conn.rollback()
                return False

            conn.commit()
            return True
        finally:
            conn.close()

    def return_my_rental(self):
        if not self.current_user or self.current_user.is_admin():
            print("Only logged-in clients can return their rentals.")
            return

        conn = self.db.connect()
        cur = conn.cursor()
        # Show only this user's rentals that are confirmed (=1)
        cur.execute("""
            SELECT r.ID, c.Brand || ' ' || c.Model AS Car, r.DateTime, r.Hours, r.Total, r.Status
            FROM rents r
            JOIN cars c ON c.ID = r.Car
            WHERE r.User=? AND r.Status=1
            ORDER BY r.DateTime DESC
        """, (self.current_user.id,))
        rows = cur.fetchall()
        conn.close()

        if not rows:
            print("You have no active (confirmed) rentals to return.")
            return

        print("\nYour Active Rentals:")
        for r in rows:
            print(f"[{r['ID']}] {r['Car']} | {r['DateTime']} | {r['Hours']}h | ${r['Total']:.2f}")

        try:
            rent_id = int(input("Enter Rental ID to return: ").strip())
        except ValueError:
            print("Invalid ID.")
            return

        # Ensure the rental belongs to the current user and is confirmed
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("SELECT ID FROM rents WHERE ID=? AND User=? AND Status=1", (rent_id, self.current_user.id))
        ok = cur.fetchone()
        conn.close()

        if not ok:
            print("Rental not found or not eligible for return.")
            return

        if self._undo_rent_transactional(rent_id):
            print("Rental returned successfully.")

    def admin_cancel_rental(self):
        if not self._ensure_admin():
            return

        # list recent confirmed rents
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.ID, u.FirstName || ' ' || u.LastName AS Client,
                   c.Brand || ' ' || c.Model AS Car,
                   r.DateTime, r.Hours, r.Total, r.Status
            FROM rents r
            JOIN users u ON u.ID = r.User
            JOIN cars  c ON c.ID = r.Car
            WHERE r.Status=1
            ORDER BY r.DateTime DESC
            LIMIT 20
        """)
        rows = cur.fetchall()
        conn.close()

        print("\nRecent Confirmed Rentals:")
        for r in rows:
            print(f"[{r['ID']}] {r['Client']} | {r['Car']} | {r['DateTime']} | {r['Hours']}h | ${r['Total']:.2f}")

        try:
            rent_id = int(input("Enter Rental ID to cancel/undo: ").strip())
        except ValueError:
            print("Invalid ID.")
            return

        if self._undo_rent_transactional(rent_id):
            print("Rental cancelled/undone and stock restored.")

    # -------------------- ADMIN: CARS --------------------
    def admin_add_car(self):
        if not self._ensure_admin():
            return
        try:
            brand = input("Brand: ").strip()
            model = input("Model: ").strip()
            color = input("Color: ").strip()
            year = int(input("Year: ").strip())
            price = float(input("Price per hour: ").strip())
            available = int(input("Available quantity: ").strip())
        except ValueError:
            print("Invalid values.")
            return

        if not all([brand, model, color]) or year < 1886 or price < 0 or available < 0:
            print("Please provide valid values.")
            return

        conn = self.db.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO cars(Brand, Model, Color, Year, Price, Available)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (brand, model, color, year, price, available))
            conn.commit()
            print("Car added successfully!")
        except sqlite3.IntegrityError as e:
            if "idx_cars_brand_model_year_color" in str(e) or "UNIQUE" in str(e):
                print("Duplicate car (Brand, Model, Year, Color) — not added.")
            else:
                print(f"Could not add car: {e}")
        finally:
            conn.close()

    def admin_update_car(self):
        if not self._ensure_admin():
            return

        self.view_cars()
        try:
            car_id = int(input("Enter Car ID to update: ").strip())
        except ValueError:
            print("Invalid ID.")
            return

        field = input(f"Field {sorted(self.ADMIN_EDITABLE_CAR_FIELDS)}: ").strip()
        if field not in self.ADMIN_EDITABLE_CAR_FIELDS:
            print("Field not allowed.")
            return
        value_raw = input("New value: ").strip()

        # Cast depending on field
        try:
            if field in {"Year", "Available"}:
                value = int(value_raw)
            elif field in {"Price"}:
                value = float(value_raw)
            else:
                value = value_raw
        except ValueError:
            print("Invalid value for the selected field.")
            return

        conn = self.db.connect()
        cur = conn.cursor()
        try:
            cur.execute(f"UPDATE cars SET {field}=? WHERE ID=?", (value, car_id))
            if cur.rowcount == 0:
                print("No car updated (check ID).")
            else:
                print("Car updated successfully!")
            conn.commit()
        except sqlite3.IntegrityError as e:
            if "idx_cars_brand_model_year_color" in str(e) or "UNIQUE" in str(e):
                print("Update violates car uniqueness (Brand, Model, Year, Color).")
            else:
                print(f"Update failed: {e}")
        finally:
            conn.close()

    def admin_delete_car(self):
        if not self._ensure_admin():
            return

        self.view_cars()
        try:
            car_id = int(input("Enter Car ID to delete: ").strip())
        except ValueError:
            print("Invalid ID.")
            return

        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM cars WHERE ID=?", (car_id,))
        if cur.rowcount == 0:
            print("No car deleted (check ID).")
        else:
            print("Car deleted successfully!")
        conn.commit()
        conn.close()

    # -------------------- ADMIN: USERS --------------------
    def admin_add_user(self):
        if not self._ensure_admin():
            return

        fname = input("First Name: ").strip()
        lname = input("Last Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        password = input("Password: ").strip()
        try:
            user_type = int(input("Type (1=Admin, 0=Client): ").strip())
            if user_type not in (0, 1):
                raise ValueError
        except ValueError:
            print("Type must be 0 or 1.")
            return

        if not all([fname, lname, email, phone, password]):
            print("All fields are required.")
            return

        conn = self.db.connect()
        cur = conn.cursor()
        try:
            cur.execute("""
                INSERT INTO users(FirstName, LastName, Email, PhoneNumber, Password, Type)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fname, lname, email, phone, _hash_password(password), user_type))
            conn.commit()
            print("User added successfully!")
        except sqlite3.IntegrityError as e:
            print(f"Could not add user: {e}")
        finally:
            conn.close()

    def admin_update_user(self):
        if not self._ensure_admin():
            return

        self.admin_list_users()
        try:
            user_id = int(input("Enter User ID to update: ").strip())
        except ValueError:
            print("Invalid ID.")
            return

        field = input(f"Field {sorted(self.ADMIN_EDITABLE_USER_FIELDS)}: ").strip()
        if field not in self.ADMIN_EDITABLE_USER_FIELDS:
            print("Field not allowed.")
            return
        value_raw = input("New value: ").strip()

        # Cast
        try:
            if field == "Type":
                value = int(value_raw)
                if value not in (0, 1):
                    raise ValueError
            elif field == "Password":
                value = _hash_password(value_raw)
            else:
                value = value_raw
        except ValueError:
            print("Invalid value for the selected field.")
            return

        conn = self.db.connect()
        cur = conn.cursor()
        try:
            cur.execute(f"UPDATE users SET {field}=? WHERE ID=?", (value, user_id))
            if cur.rowcount == 0:
                print("No user updated (check ID).")
            else:
                print("User updated successfully!")
            conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"Update failed: {e}")
        finally:
            conn.close()

    def admin_delete_user(self):
        if not self._ensure_admin():
            return

        self.admin_list_users()
        try:
            user_id = int(input("Enter User ID to delete: ").strip())
        except ValueError:
            print("Invalid ID.")
            return

        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE ID=?", (user_id,))
        if cur.rowcount == 0:
            print("No user deleted (check ID).")
        else:
            print("User deleted successfully!")
        conn.commit()
        conn.close()

    def admin_list_users(self):
        if not self._ensure_admin():
            return
        conn = self.db.connect()
        cur = conn.cursor()
        cur.execute("SELECT ID, FirstName, LastName, Email, Type FROM users ORDER BY ID")
        users = cur.fetchall()
        conn.close()

        print("\nUsers:")
        for u in users:
            role = "Admin" if u["Type"] == 1 else "Client"
            print(f"[{u['ID']}] {u['FirstName']} {u['LastName']} - {u['Email']} ({role})")

    # -------------------- HELPERS --------------------
    def _ensure_admin(self) -> bool:
        if not self.current_user:
            print("You must log in first.")
            return False
        if not self.current_user.is_admin():
            print("Admin privileges required.")
            return False
        return True

    # -------------------- MAIN LOOP (Logout -> Main Menu) --------------------
    def run(self):
        print("=== Car Rental System CLI (Admin Manage Cars & Users) ===")

        while True:
            # ---------- MAIN MENU (shown whenever no one is logged in) ----------
            while self.current_user is None:
                print("\n1. Login\n2. Register\n3. Exit")
                choice = input("Choice: ").strip()
                if choice == "1":
                    self.login()      # sets self.current_user on success
                elif choice == "2":
                    self.register()
                elif choice == "3":
                    return
                else:
                    print("Invalid choice.")

            # ---------- ROLE MENUS (shown only when logged in) ----------
            if self.current_user.is_admin():
                # --- ADMIN MENU ---
                while self.current_user is not None and self.current_user.is_admin():
                    print("""
=== Admin Menu ===
1. View Cars
2. Add Car
3. Update Car
4. Delete Car
5. View All Rents
6. List Users
7. Add User
8. Update User
9. Delete User
10. Cancel/Undo Rental
11. Logout
""")
                    choice = input("Choice: ").strip()
                    if choice == "1": self.view_cars()
                    elif choice == "2": self.admin_add_car()
                    elif choice == "3": self.admin_update_car()
                    elif choice == "4": self.admin_delete_car()
                    elif choice == "5": self.view_rents(all_users=True)
                    elif choice == "6": self.admin_list_users()
                    elif choice == "7": self.admin_add_user()
                    elif choice == "8": self.admin_update_user()
                    elif choice == "9": self.admin_delete_user()
                    elif choice == "10": self.admin_cancel_rental()
                    elif choice == "11":
                        print("=== Car Rental System CLI (Admin Manage Cars & Users) ===")
                        self.current_user = None  # back to MAIN MENU
                    else:
                        print("Invalid choice.")
            else:
                # --- CLIENT MENU ---
                while self.current_user is not None and not self.current_user.is_admin():
                    print("""
=== Client Menu ===
1. View Cars
2. Rent Car
3. View My Rents
4. Return a Rental
5. Logout
""")
                    choice = input("Choice: ").strip()
                    if choice == "1": self.view_cars()
                    elif choice == "2": self.rent_car()
                    elif choice == "3": self.view_rents()
                    elif choice == "4": self.return_my_rental()
                    elif choice == "5":
                        print("=== Car Rental System CLI (Admin Manage Cars & Users) ===")
                        self.current_user = None  # back to MAIN MENU
                    else:
                        print("Invalid choice.")


if __name__ == "__main__":
    system = CarRentalSystem()
    system.run()
