"""
Django forms.
"""
from django import forms


class TemperatureForm(forms.Form):
    """Temperature conversion form."""

    temperature = forms.FloatField(
        label='Temperature',
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )

    from_unit = forms.ChoiceField(
        label='From',
        choices=[
            ('celsius', 'Celsius (°C)'),
            ('fahrenheit', 'Fahrenheit (°F)'),
            ('kelvin', 'Kelvin (K)'),
        ]
    )

    to_unit = forms.ChoiceField(
        label='To',
        choices=[
            ('celsius', 'Celsius (°C)'),
            ('fahrenheit', 'Fahrenheit (°F)'),
            ('kelvin', 'Kelvin (K)'),
        ]
    )