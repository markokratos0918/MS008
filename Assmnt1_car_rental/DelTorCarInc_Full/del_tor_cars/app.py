from __future__ import annotations
from typing import Optional
from del_tor_cars.db import Database
from del_tor_cars.models import User
from del_tor_cars.factories import build_bundles, SqliteRepoFactory, ServicesBundle, ReposBundle, DefaultServiceFactory
from del_tor_cars.utils import parse_date
from del_tor_cars.errors import AppError

class App:
    def __init__(self):
        self.db = Database()  # Or a db_factory if you added one
        repos, svcs = build_bundles(self.db, SqliteRepoFactory(), DefaultServiceFactory("dynamic"))
        self.user_repo: ReposBundle = repos.users
        self.car_repo:  ReposBundle = repos.cars
        self.rental_repo: ReposBundle = repos.rentals
        self.auth:    ServicesBundle = svcs.auth
        self.booking: ServicesBundle = svcs.booking
        self.admin_svc: ServicesBundle = svcs.admin
        self.current_user: Optional[User] = None

    def view_cars(self):
        cars = self.car_repo.available(); print("\n=== Available Cars ===")
        for c in cars:
            print(f"[{c.id}] {c.make} {c.model} {c.color} {c.year} | {c.mileage} km | $ {c.daily_rate:.2f}/day | stock:{c.available_now} | {c.min_days}-{c.max_days} days")
        if not cars: print("No cars available right now.")

    def make_booking(self):
        if not self.current_user or self.current_user.is_admin(): print("Only logged-in customers can book."); return
        self.view_cars()
        try: car_id = int(input("Car ID: ").strip())
        except ValueError: print("Invalid car id."); return
        start = parse_date(input("Start date (YYYY-MM-DD): ").strip())
        end = parse_date(input("End date   (YYYY-MM-DD): ").strip())
        if not start or not end: print("Invalid dates."); return
        try: extras = float(input("Extras/charges (0 for none): ").strip() or "0")
        except ValueError: print("Invalid extras value."); return
        try:
            rid = self.booking.create_booking(self.current_user.id, car_id, start, end, extras)
            print(f"Booking #{rid} created as PENDING.")
        except AppError as e: print(e)

    def my_rentals(self):
        if not self.current_user: print("Login first."); return
        rows = self.rental_repo.list_for_user(self.current_user.id); print("\n=== My Rentals ===")
        for r in rows:
            print(f"[{r['id']}] {r['car']} | {r['start_date']} → {r['end_date']} | {r['days']}d | $ {r['grand_total']:.2f} | {r['status']}")
        if not rows: print("No rentals yet.")

    def return_rental(self):
        if not self.current_user or self.current_user.is_admin(): print("Only logged-in customers can return."); return
        self.my_rentals()
        try: rid = int(input("Enter approved Rental ID to return: ").strip())
        except ValueError: print("Invalid ID."); return
        if self.rental_repo.return_rental(rid, for_user_id=self.current_user.id): print("Return successful. Thank you!")
        else: print("Return failed. Ensure the rental is approved and belongs to you.")

    def list_all_rentals(self):
        rows = self.rental_repo.list_all(); print("\n=== All Rentals ===")
        for r in rows:
            print(f"[{r['id']}] {r['customer']} | {r['car']} | {r['start_date']}→{r['end_date']} | {r['days']}d | $ {r['grand_total']:.2f} | {r['status']}")
        if not rows: print("No rentals found.")

    def approve_reject(self):
        if not self._admin_only(): return
        self.list_all_rentals()
        try: rid = int(input("Rental ID: ").strip())
        except ValueError: print("Invalid ID."); return
        action = input("Approve (A) / Reject (R): ").strip().lower()
        if action == "a": print("Approved." if self.admin_svc.approve(rid) else "Could not approve (check status/stock).")
        elif action == "r": print("Rejected." if self.admin_svc.reject(rid) else "Could not reject (check status).")
        else: print("Unknown action.")

    def manage_cars(self):
        if not self._admin_only(): return
        while True:
            print("""
=== Car Management (Admin) ===
1. List cars
2. Add car
3. Update car field
4. Delete car
5. Back
""")
            c = input("Choice: ").strip()
            if c == "1":
                for car in self.car_repo.all():
                    print(f"[{car.id}] {car.make} {car.model} {car.color} {car.year} | {car.mileage} km | $ {car.daily_rate:.2f}/day | stock:{car.available_now} | {car.min_days}-{car.max_days}d")
            elif c == "2":
                try:
                    make = input("Make: ").strip(); model = input("Model: ").strip(); color = input("Color: ").strip()
                    year = int(input("Year: ")); mileage = int(input("Mileage (km): ")); rate = float(input("Daily rate: "))
                    stock = int(input("Available now: ")); min_d = int(input("Min days: ")); max_d = int(input("Max days: "))
                except ValueError: print("Invalid values."); continue
                try:
                    from .errors import AppError
                    self.admin_svc.add_car(make, model, color, year, mileage, rate, stock, min_d, max_d); print("Car added.")
                except AppError as e: print(e)
                except Exception as e: print(f"Add failed: {e}")
            elif c == "3":
                try:
                    cid = int(input("Car ID: ")); field = input("Field (make,model,color,year,mileage,daily_rate,available_now,min_days,max_days): ").strip()
                    raw = input("New value: ").strip()
                    if field in {"year","mileage","available_now","min_days","max_days"}: val = int(raw)
                    elif field in {"daily_rate"}: val = float(raw)
                    else: val = raw
                except ValueError: print("Invalid input."); continue
                print("Updated." if self.car_repo.update_field(cid, field, val) else "No update (check field/ID).")
            elif c == "4":
                try: cid = int(input("Car ID: "))
                except ValueError: print("Invalid ID."); continue
                print("Deleted." if self.car_repo.delete(cid) else "No delete (check ID).")
            elif c == "5": break
            else: print("Invalid choice.")

    def manage_users(self):
        if not self._admin_only(): return
        while True:
            print("""
=== User Management (Admin) ===
1. List users
2. Add user
3. Update role
4. Delete user
5. Back
""")
            c = input("Choice: ").strip()
            if c == "1":
                for u in self.user_repo.list_users():
                    print(f"[{u['id']}] {u['first_name']} — {u['email']} ({u['role']})")
            elif c == "2":
                first = input("First: ").strip(); last = input("Last: ").strip(); email = input("Email: ").strip(); phone = input("Phone: ").strip(); pw = input("Password: ").strip()
                role = input("Role (admin/customer): ").strip()
                if role not in ("admin","customer") or not all([first,last,email,phone,pw]): print("Invalid values."); continue
                try: self.user_repo.add_user(first,last,email,phone,pw,role); print("User added.")
                except Exception as e: print(f"Add failed: {e}")
            elif c == "3":
                try: uid = int(input("User ID: ")); role = input("New role (admin/customer): ").strip(); 
                except ValueError: print("Invalid input."); continue
                if role not in ("admin","customer"): print("Invalid input."); continue
                print("Updated." if self.user_repo.update_role(uid, role) else "No update (check ID).")
            elif c == "4":
                try: uid = int(input("User ID: "))
                except ValueError: print("Invalid ID."); continue
                print("Deleted." if self.user_repo.delete(uid) else "No delete (check ID).")
            elif c == "5": break
            else: print("Invalid choice.")

    def _admin_only(self) -> bool:
        if not self.current_user: print("Login first."); return False
        if not self.current_user.is_admin(): print("Admin privileges required."); return False
        return True

    def _main_menu(self):
        while self.current_user is None:
            print("\n1. Login\n2. Register\n3. Exit"); ch = input("Choice: ").strip()
            if ch == "1": self.current_user = self.auth.login()
            elif ch == "2": self.auth.register()
            elif ch == "3": raise SystemExit
            else: print("Invalid choice.")

    def _customer_menu(self):
        while self.current_user and not self.current_user.is_admin():
            print("""
=== Customer Menu ===
1. View available cars
2. Make booking
3. My rentals
4. Return rental
5. Logout
""")
            ch = input("Choice: ").strip()
            if ch == "1": self.view_cars()
            elif ch == "2": self.make_booking()
            elif ch == "3": self.my_rentals()
            elif ch == "4": self.return_rental()
            elif ch == "5": self.current_user = None
            else: print("Invalid choice.")

    def _admin_menu(self):
        while self.current_user and self.current_user.is_admin():
            print("""
=== Admin Menu ===
1. Car management
2. User management
3. View all rentals
4. Approve/Reject rental
5. Logout
""")
            ch = input("Choice: ").strip()
            if ch == "1": self.manage_cars()
            elif ch == "2": self.manage_users()
            elif ch == "3": self.list_all_rentals()
            elif ch == "4": self.approve_reject()
            elif ch == "5": self.current_user = None
            else: print("Invalid choice.")

    def run(self):
        print("=== DelTor Car Inc. — CLI ===")
        while True:
            self._main_menu()
            if self.current_user and self.current_user.is_admin(): self._admin_menu()
            elif self.current_user: self._customer_menu()

def main():
    App().run()

if __name__ == "__main__":
    main()
