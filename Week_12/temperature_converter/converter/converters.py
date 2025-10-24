"""
Temperature conversion logic.
"""
from abc import ABC, abstractmethod
from .temperature_units import TemperatureUnit


class ConversionStrategy(ABC):
    """Base class for conversions."""

    @abstractmethod
    def convert(self, temperature):
        """Convert temperature."""


class CelsiusToFahrenheit(ConversionStrategy):
    """C to F: F = (C × 9/5) + 32"""

    def convert(self, temperature):
        """Convert Celsius to Fahrenheit."""
        return (temperature * 9 / 5) + 32


class CelsiusToKelvin(ConversionStrategy):
    """C to K: K = C + 273.15"""

    def convert(self, temperature):
        """Convert Celsius to Kelvin."""
        return temperature + 273.15


class FahrenheitToCelsius(ConversionStrategy):
    """F to C: C = (F - 32) × 5/9"""

    def convert(self, temperature):
        """Convert Fahrenheit to Celsius."""
        return (temperature - 32) * 5 / 9


class FahrenheitToKelvin(ConversionStrategy):
    """F to K: K = (F - 32) × 5/9 + 273.15"""

    def convert(self, temperature):
        """Convert Fahrenheit to Kelvin."""
        return (temperature - 32) * 5 / 9 + 273.15


class KelvinToCelsius(ConversionStrategy):
    """K to C: C = K - 273.15"""

    def convert(self, temperature):
        """Convert Kelvin to Celsius."""
        return temperature - 273.15


class KelvinToFahrenheit(ConversionStrategy):
    """K to F: F = (K - 273.15) × 9/5 + 32"""

    def convert(self, temperature):
        """Convert Kelvin to Fahrenheit."""
        return (temperature - 273.15) * 9 / 5 + 32


class IdentityStrategy(ConversionStrategy):
    """Same unit conversion."""

    def convert(self, temperature):
        """Return same value."""
        return temperature


class TemperatureConverter:
    """Main converter class."""

    CONVERSION_MAP = {
        (TemperatureUnit.CELSIUS, TemperatureUnit.FAHRENHEIT): CelsiusToFahrenheit(),
        (TemperatureUnit.CELSIUS, TemperatureUnit.KELVIN): CelsiusToKelvin(),
        (TemperatureUnit.FAHRENHEIT, TemperatureUnit.CELSIUS): FahrenheitToCelsius(),
        (TemperatureUnit.FAHRENHEIT, TemperatureUnit.KELVIN): FahrenheitToKelvin(),
        (TemperatureUnit.KELVIN, TemperatureUnit.CELSIUS): KelvinToCelsius(),
        (TemperatureUnit.KELVIN, TemperatureUnit.FAHRENHEIT): KelvinToFahrenheit(),
    }

    def __init__(self, precision=2):
        """Initialize converter."""
        self.precision = precision

    def convert(self, temperature, from_unit, to_unit):
        """Convert temperature between units."""
        if from_unit == to_unit:
            strategy = IdentityStrategy()
        else:
            strategy = self.CONVERSION_MAP.get((from_unit, to_unit))
            if strategy is None:
                raise ValueError(f"Unsupported conversion")

        result = strategy.convert(temperature)
        return round(result, self.precision)
