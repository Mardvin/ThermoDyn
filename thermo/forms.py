from django.core.exceptions import ValidationError
from datetime import date

from django import forms
from .models import Home

class AddHomeForm(forms.ModelForm):

    class Meta:
        model = Home
        fields = ['street_name', 'numbers', 'construction_volume', 'indoor_air_temperature', 'construction_year']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    # def clean_construction_year(self):
    #     year = self.cleaned_data['year']
    #     current_year = date.today().year
    #
    #     if year > current_year:
    #         raise ValidationError(f"Год не может быть больше {current_year}")
    #
    #     return year