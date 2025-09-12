
from typing import Optional
from .db import Database
from .models import User
from .repos import UserRepo, CarRepo, RentalRepo
from .services import AuthService, BookingService, AdminService
from .utils import parse_date
from .errors import AppError

class App:

    def __init__(self):
        self.db = Database()
        self.user_repo = UserRepo(self.db)
        self.car_repo = UserRepo(self.db)
        self.rental_repo = RentalRepo(self.db)
        self.auth = AuthService(self.user_repo)
        self.booking = BookingService(self.db, self.rental_repo)
        self.admin_svc = AdminService(self.user_repo, self.car_repo, self.rental_repo)
        self.current_user: Optional[User] = None


    # -------- Customer features --------

    def view_cars(self):
        cars = self.car_repo.available()
        print("\n=== Available Cars ===")
        for car in cars:
            print(f"[{c.id}] {c.make} {c.model} {c.color} {c.year} | "
                f"{c.mileage} km | $ {c.daily_rate:.2f}/day | "
                f"stock:{c.available_now} | {c.min_days}-{c.max_days} days"
           )
        if not cars:
            print("Sorry, No cars available right now.")  

    def make_booking(self):
        if not self.current_user or self.current_user.is_admin():
            print("Only logged-in customers can book.")
            return
        self.view_cars()
        try:
            car_id = int(input("Car ID: ").strip())
        except ValueError:
            print("Invalid car id.")
            return    
        start = parse_date(input("Start date (YYYY-MM-DD): ").strip())
        end = parse_date(input("End date   (YYYY-MM-DD): ").strip())

        if not start or not end:
            print("Invalid dates.")
            return

        try:
            extras = float(input("Extras/charges (0 for none): ").strip() or "0")
        except ValueError:
            print("Invalid extras value.")
            return
        try:
            rid = self.booking.create_booking(self.current_user.id, car_id, start, end, extras)
            print(f"Booking #{rid} created as PENDING.")
        except AppError as e:
            print(e)   
    def my_rentals(self):
        if not self.current_user:
            print("Login first.")
            return
        rows = self.rental_repo.list_for_user(self.current_user.id)
        print("\n=== My Rentals ===")
        for r in rows:
            print(
                f"[{r['id']}] {r['car']} | {r['start_date']} → {r['end_date']} | "
                f"{r['days']}d | $ {r['grand_total']:.2f} | {r['status']}"
            )
        if not rows:
               print("No rentals yet.")
    
    def return_rental(self):
        if not self.current_user or self.current_user.is_admin():
            print("Only logged-in customers can return.")
            return
        self.my_rentals()
        try:
            rid = int(input("Enter approved Rental ID to return: ").strip())
        except ValueError:
            print("Invalid ID.")
            return
        if self.rental_repo.return_rental(rid, for_user_id=self.current_user.id):
            print("Return successful. Thank you!")
        else:
            print("Return failed. Ensure the rental is approved and belongs to you.")
        
    # -------- Admin features --------
    def list_all_rentals(self):
        rows = self.rental_repo.list_all()
        print("\n=== All Rentals ===")
        for r in rows:
            print(
                f"[{r['id']}] {r['customer']} | {r['car']} | "
                f"{r['start_date']}→{r['end_date']} | {r['days']}d | "
                f"$ {r['grand_total']:.2f} | {r['status']}"
            )
        
        if not rows:
            print("No rentals found.")

    def approve_reject(self):
        if not self._admin_only():
            return
        self.list_all_rentals()
        try:
            rid = int(input("Enter the Rental ID: ").strip())
        except ValueError:
            print("Invalid ID.")
            return
        action = input("Approve (A) / Reject (R): ").strip().lower()
        if action == "a":
            print("Approved." if self.admin_svc.approve(rid) else "Could not approve (check status/stock).")
        elif action == "r":
            print("Rejected." if self.admin_svc.reject(rid) else "Could not reject (check status).")
        else:
            print("Unknown action.")
    
    def manage_cars(self):
        if not self._admin_only():
            return
        while True:
            print(
                """
=== Car Management (Admin) ===
1. List cars
2. Add car
3. Update car info
4. Delete car
5. Back
"""         )
            
            c = input("Choice: ").strip()
            if c == "1":
                for car in self.car_repo.all():
                    print(
                        f"[{car.id}] {car.make} {car.model} {car.color} {car.year} | "
                        f"{car.mileage} km | $ {car.daily_rate:.2f}/day | "
                        f"stock:{car.available_now} | {car.min_days}-{car.max_days}d"
                    )
            elif c == "2":
                try:
                    make = input("Make: ").strip()
                    model = input("Model: ").strip()
                    color = input("Color: ").strip()
                    year = int(input("Year: "))
                    mileage = int(input("Mileage (km): "))
                    rate = float(input("Daily rate: "))
                    stock = int(input("Available now: "))
                    min_d = int(input("Min days: "))
                    max_d = int(input("Max days: "))
                except ValueError:
                    print("Invalid values.")
                    continue   
                try:
                    from .errors import AppError
                    self.admin_svc.add_car(make, model, color, year, mileage, rate, stock, min_d, max_d)
                    print("Car added.")
                except AppError as e:
                    print(e)
                except Exception as e:
                    print(f"Add failed: {e}")
            
            elif c == "3":
                try:
                    cid = int(input("Car ID: "))
                    field = input("Field (make,model,color,year,mileage,daily_rate,available_now,min_days,max_days): ").strip()
                    raw = input("New value: ").strip()
                    if field in {"year", "mileage", "available_now", "min_days", "max_days"}:
                        val = int(raw)
                    elif field in {"daily_rate"}:
                        val = float(raw)
                    else:
                        val = raw
                except ValueError:
                    print("Invalid input.")
                    continue
                print("Updated." if self.car_repo.update_field(cid, field, val) else "No update (check field/ID).")
            elif c == "4":
                try:
                    cid = int(input("Car ID: "))
                except ValueError:
                    print("Invalid ID.")
                    continue
                print("Deleted." if self.car_repo.delete(cid) else "No delete (check ID).")
            elif c == "5":
                break
            else:
                print("Invalid choice.")