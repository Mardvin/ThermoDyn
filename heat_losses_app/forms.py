from django import forms
from .models import PipelineSegment


class AddPipeLineSegment(forms.ModelForm):

    class Meta:
        model = PipelineSegment
        fields = ['diameter', 'length', 'insulation_material', 'laying_type', 'commissioning_year']
