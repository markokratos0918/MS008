from __future__ import annotations
from abc import ABC, abstractmethod
import hashlib

class HashingStrategy(ABC):
    @abstractmethod
    def hash(self, raw: str) -> str: ...
    @abstractmethod
    def verify(self, raw: str, hashed: str) -> bool: ...

class Sha256Hash(HashingStrategy):
    def hash(self, raw: str) -> str:
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
    def verify(self, raw: str, hashed: str) -> bool:
        return self.hash(raw) == hashed

# Future:
# class BcryptHash(HashingStrategy): ...

class HashingFactory:
    @staticmethod
    def get(mode: str = "sha256") -> HashingStrategy:
        # Could switch to bcrypt/argon2 later
        return Sha256Hash()
