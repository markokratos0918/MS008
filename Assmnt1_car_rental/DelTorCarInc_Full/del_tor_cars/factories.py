from __future__ import annotations
from dataclasses import dataclass
from del_tor_cars.db import Database
from del_tor_cars.ifaces import AbstractRepoFactory, AbstractServiceFactory
from del_tor_cars.repos.user_repo import UserRepo
from del_tor_cars.repos.car_repo import CarRepo
from del_tor_cars.repos.rental_repo import RentalRepo
from del_tor_cars.services.auth_service import AuthService
from del_tor_cars.services.booking_service import BookingService
from del_tor_cars.services.admin_service import AdminService
from del_tor_cars.hashing import HashingFactory
from del_tor_cars.pricing import PricingFactory, PricingStrategy

@dataclass
class ReposBundle:
    users: UserRepo
    cars: CarRepo
    rentals: RentalRepo

@dataclass
class ServicesBundle:
    auth: AuthService
    booking: BookingService
    admin: AdminService

class SqliteRepoFactory(AbstractRepoFactory):
    """Factory Method: create SQLite-backed repositories."""
    def __init__(self, hasher_mode: str = "sha256"):
        self._hasher = HashingFactory.get(hasher_mode)

    def users(self, db: Database) -> UserRepo:
        return UserRepo(db, hasher=self._hasher)

    def cars(self, db: Database) -> CarRepo:
        return CarRepo(db)

    def rentals(self, db: Database) -> RentalRepo:
        return RentalRepo(db)

class DefaultServiceFactory(AbstractServiceFactory):
    """Factory Method: create services with injected strategies."""
    def __init__(self, pricing_mode: str = "standard"):
        self._pricing: PricingStrategy = PricingFactory.get(pricing_mode)

    def auth(self, repos: tuple[UserRepo, CarRepo, RentalRepo]) -> AuthService:
        users, _, _ = repos
        return AuthService(users)

    def booking(self, db: Database, rentals: RentalRepo) -> BookingService:
        return BookingService(db, rentals, pricing=self._pricing)

    def admin(self, repos: tuple[UserRepo, CarRepo, RentalRepo]) -> AdminService:
        users, cars, rentals = repos
        return AdminService(users, cars, rentals)

def build_bundles(
    db: Database,
    repo_factory: AbstractRepoFactory,
    svc_factory: AbstractServiceFactory,
) -> tuple[ReposBundle, ServicesBundle]:
    """Single composition point used by the UI layer."""
    users = repo_factory.users(db)
    cars = repo_factory.cars(db)
    rentals = repo_factory.rentals(db)
    repos = ReposBundle(users, cars, rentals)
    svcs = ServicesBundle(
        auth=svc_factory.auth((users, cars, rentals)),
        booking=svc_factory.booking(db, rentals),
        admin=svc_factory.admin((users, cars, rentals)),
    )
    return repos, svcs
