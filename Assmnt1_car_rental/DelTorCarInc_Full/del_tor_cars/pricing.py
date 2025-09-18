from __future__ import annotations
from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calc(self, days: int, daily_rate: float, extras: float = 0.0) -> tuple[float, float, float]: ...

class StandardPricing(PricingStrategy):
    def calc(self, days, daily_rate, extras=0.0):
        base = round(days * daily_rate, 2)
        extras_total = round(extras, 2)
        return base, extras_total, round(base + extras_total, 2)

class DynamicPricing(PricingStrategy):
    def __init__(self, surge: float = 1.15):  # demo: +15%
        self.surge = surge
    def calc(self, days, daily_rate, extras=0.0):
        base = round(days * daily_rate * self.surge, 2)
        extras_total = round(extras, 2)
        return base, extras_total, round(base + extras_total, 2)

class PricingFactory:
    @staticmethod
    def get(mode: str = "standard") -> PricingStrategy:
        if mode == "dynamic":
            return DynamicPricing()
        return StandardPricing()
