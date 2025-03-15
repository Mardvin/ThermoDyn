from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from thermo.forms import AddElectricityForm
from thermo.models import BoilerRoomPump


class ElectricityCosts(ListView):
    model = BoilerRoomPump
    template_name = 'thermo/electricity_costs.html'
    context_object_name = 'pumps'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Расчет затрат электроэнергии'
        return context


class CreateElectricity(CreateView):
    form_class = AddElectricityForm
    template_name = 'thermo/create_electricity_costs.html'
    success_url = reverse_lazy('electricity_costs')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UpdateElectricity(UpdateView):
    model = BoilerRoomPump
    form_class = AddElectricityForm
    template_name = 'thermo/create_electricity_costs.html'
    success_url = reverse_lazy('electricity_costs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteElectricity(DeleteView):
    model = BoilerRoomPump
    template_name = 'thermo/electricity_costs.html'
    success_url = reverse_lazy('electricity_costs')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        """Переопределяем post, чтобы сразу удалять без подтверждения"""
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)
