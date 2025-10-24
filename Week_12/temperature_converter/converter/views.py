"""
Views for converter app.
"""
from django.shortcuts import render
from django.views import View
from .forms import TemperatureForm
from .converters import TemperatureConverter
from .temperature_units import TemperatureUnit


class ConverterView(View):
    """Main converter view."""

    template_name = 'converter/index.html'  # ← CHANGE THIS LINE
    form_class = TemperatureForm

    def __init__(self, **kwargs):
        """Initialize view."""
        super().__init__(**kwargs)
        self.converter = TemperatureConverter()

    def get(self, request):
        """Handle GET request."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Handle POST request."""
        form = self.form_class(request.POST)
        result = None
        error = None

        if form.is_valid():
            try:
                data = form.cleaned_data
                temp = data['temperature']
                from_u = TemperatureUnit.from_string(data['from_unit'])
                to_u = TemperatureUnit.from_string(data['to_unit'])
                result = self.converter.convert(temp, from_u, to_u)
            except Exception as exc:
                error = str(exc)

        context = {'form': form, 'result': result, 'error': error}
        return render(request, self.template_name, context)