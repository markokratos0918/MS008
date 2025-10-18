class TemperatureConverter:
    """Handles temperature conversions between Celsius, Fahrenheit, and Kelvin."""

    @staticmethod
    def to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return celsius * 9.0 / 5.0 + 32

    @staticmethod
    def to_celsius_f(from_unit: str, temp: float) -> float:
        """Convert Fahrenheit or Kelvin to Celsius."""
        if from_unit == 'Fahrenheit':
            return (temp - 32) * 5.0 / 9.0
        if from_unit == 'Kelvin':
            return temp - 273.15
        return temp

    @staticmethod
    def to_kelvin(from_unit: str, temp: float) -> float:
        """Convert Celsius or Fahrenheit to Kelvin."""
        if from_unit == 'Fahrenheit':
            return (temp - 32) * 5.0 / 9.0 + 273.15
        if from_unit == 'Celsius':
            return temp + 273.15
        return temp

    def convert(self, value: float, from_unit: str, to_unit: str) -> float:
        """Convert value from one temperature unit to another."""
        if from_unit == to_unit:
            return value
        if to_unit == 'Celsius':
            return self.to_celsius_f(from_unit, value)
        if to_unit == 'Fahrenheit':
            if from_unit == 'Celsius':
                return self.to_fahrenheit(value)
            if from_unit == 'Kelvin':
                # Kelvin to Fahrenheit
                return (value - 273.15) * 9.0 / 5.0 + 32
            if from_unit == 'Fahrenheit':
                return value
        if to_unit == 'Kelvin':
            return self.to_kelvin(from_unit, value)
        raise ValueError(f"Cannot convert {from_unit} to {to_unit}")
