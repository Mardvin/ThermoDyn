from django import forms

from heat_losses_app.models import HeatLossInsulation
from heat_losses_app.models.models import PipelineSegment


class AddPipeLineSegment(forms.ModelForm):

    class Meta:
        model = PipelineSegment
        fields = ['diameter', 'length', 'insulation_material', 'laying_type', 'commissioning_year']


class AddPipelineInsulationForm(forms.ModelForm):
    pipeline_segment = forms.ModelChoiceField(
        queryset=PipelineSegment.objects.all(),
        label="Выберите участок трубопровода",
        widget=forms.Select(attrs={"class": "form-control"}),
        to_field_name="id"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pipeline_segment'].label_from_instance = self.get_pipeline_segment_label

    def get_pipeline_segment_label(self, obj):
        return f"{obj.diameter} мм, {obj.length} км, {obj.laying_type}, {obj.insulation_material}"

    class Meta:
        model = HeatLossInsulation
        fields = ['pipeline_segment', 'insulation_thickness_mm']

