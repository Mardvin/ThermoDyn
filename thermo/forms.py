from django.core.exceptions import ValidationError
from datetime import date

from django import forms
from .models import Home, BoilerRoomPump


class AddHomeForm(forms.ModelForm):

    class Meta:
        model = Home
        fields = ['street_name', 'numbers', 'construction_volume', 'indoor_air_temperature', 'construction_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

class AddElectricityForm(forms.ModelForm):
    class Meta:
        fields = ['pump_type', 'pump_category', 'power_kW', 'operating_hours',]
        model = BoilerRoomPump
