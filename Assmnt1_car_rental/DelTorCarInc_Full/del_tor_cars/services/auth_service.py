import sqlite3
from ..repos import UserRepo
from ..validators import ensure_non_empty
from ..errors import ValidationError


class AuthService:
    def __init__(self, users: UserRepo):
        self.users = users

    def register(self) -> bool:
        print("\n=== Register (customer) ===")
        first = input("First name: ").strip()
        last = input("Last name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        password = input("Password: ").strip()
        try:
            ensure_non_empty(
                ("First name", first),
                ("Last name", last),
                ("Email", email),
                ("Phone", phone),
                ("Password", password),
            )
        except ValidationError as e:
            print(e)
            return False
        try:
            self.users.create_customer(first, last, email, phone, password)
            print("Registration successful! You can now log in.")
            return True
        except sqlite3.IntegrityError as e:
            print(f"Could not register: {e}")
            return False

    def login(self):
        print("\n=== Login ===")
        email = input("Email: ").strip(); password = input("Password: ").strip()
        user = self.users.login(email, password)
        print("Invalid credentials." if not user else f"Welcome {user.first_name}! ({user.role})")
        return user
