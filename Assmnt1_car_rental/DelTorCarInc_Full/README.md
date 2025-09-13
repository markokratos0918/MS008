# DelTor Car Inc. — Car Rental System (Full Source Release)

## How to Run
1. Install Python 3.9+
2. Unzip the package
3. Open a terminal in the unzipped folder and run:
   ```bash
   python run.py
   ```

## Default Accounts
- Admin:    admin@example.com / 0000
- Customer: alice@example.com / 1111

## Structure
- run.py — entry point
- del_tor_cars/ — application package
  - app.py, config.py, db.py, models.py, utils.py, validators.py, errors.py, __init__.py
  - repos/: user_repo.py, car_repo.py, rental_repo.py
  - services/: auth_service.py, booking_service.py, admin_service.py, fee_calculator.py
- carrentalsystem.db — SQLite database (created/seeded on first run)
