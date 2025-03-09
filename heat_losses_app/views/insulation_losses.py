from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from heat_losses_app.forms import AddPipeLineSegment, AddPipelineInsulationForm
from heat_losses_app.functions.main_heat_losses import DataRepository, main_heat_losses
from heat_losses_app.models.insulation_losses import HeatLossInsulation
from heat_losses_app.models.models import LayingType

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_data_about_home'},
    {'title': "Войти", 'url_name': 'login'},
]


class HeatLossByType:
    def __init__(self, laying_type, heat_losses):
        self.laying_type = laying_type
        self.heat_losses = heat_losses

class InsulationLossesView(ListView):
    model = HeatLossInsulation
    template_name = 'heat_losses_app/insulation_losses.html'
    context_object_name = 'segments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu

        # Получаем все виды прокладки
        context['laying_types'] = LayingType.choices

        # Фильтруем объекты HeatLossInsulation по каждому типу прокладки
        context['heat_losses_by_type'] = [
            HeatLossByType(laying_type[0], HeatLossInsulation.objects.filter(pipeline_segment__laying_type=laying_type[0]))
            for laying_type in LayingType.choices
        ]

        return context


class CreateInsulationLosses(CreateView):
    form_class = AddPipelineInsulationForm
    template_name = 'heat_losses_app/create_pipeline_insulation.html'
    success_url = reverse_lazy('insulation_losses')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
