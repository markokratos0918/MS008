from dataclasses import dataclass


@dataclass
class User:
    id: int
    first_name: str
    role: str  # 'admin' | 'customer'

    def is_admin(self) -> bool:
        return self.role == "admin"


@dataclass
class Car:
    id: int
    make: str
    model: str
    color: str
    year: int
    mileage: int
    daily_rate: float
    available_now: int
    min_days: int
    max_days: int
