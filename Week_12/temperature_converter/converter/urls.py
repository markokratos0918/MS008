"""
URL routing.
"""
from django.urls import path
from .views import ConverterView

app_name = 'converter'

urlpatterns = [
    path('', ConverterView.as_view(), name='index'),
]