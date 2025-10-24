"""
Temperature units enumeration.
"""
from enum import Enum


class TemperatureUnit(Enum):
    """Temperature unit types."""
    CELSIUS = 'celsius'
    FAHRENHEIT = 'fahrenheit'
    KELVIN = 'kelvin'

    @classmethod
    def from_string(cls, unit_string):
        """Convert string to enum."""
        for unit in cls:
            if unit.value == unit_string.lower():
                return unit
        raise ValueError(f"Invalid unit: {unit_string}")
