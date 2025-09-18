from __future__ import annotations
from abc import ABC, abstractmethod
from del_tor_cars.db import Database
from del_tor_cars.repos.user_repo import UserRepo
from del_tor_cars.repos.car_repo import CarRepo
from del_tor_cars.repos.rental_repo import RentalRepo
from del_tor_cars.services.auth_service import AuthService
from del_tor_cars.services.booking_service import BookingService
from del_tor_cars.services.admin_service import AdminService

class AbstractRepoFactory(ABC):
    @abstractmethod
    def users(self, db: Database) -> UserRepo: ...
    @abstractmethod
    def cars(self, db: Database) -> CarRepo: ...
    @abstractmethod
    def rentals(self, db: Database) -> RentalRepo: ...

class AbstractServiceFactory(ABC):
    @abstractmethod
    def auth(self, repos: tuple[UserRepo, CarRepo, RentalRepo]) -> AuthService: ...
    @abstractmethod
    def booking(self, db: Database, rentals: RentalRepo) -> BookingService: ...
    @abstractmethod
    def admin(self, repos: tuple[UserRepo, CarRepo, RentalRepo]) -> AdminService: ...
