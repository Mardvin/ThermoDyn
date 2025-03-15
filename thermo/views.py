from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from thermo.forms import AddHomeForm
from thermo.function.heat_power import total_heat_energy
from thermo.models import Home


class ThermoHome(ListView):
    model = Home
    template_name = 'thermo/result_claculations.html'
    context_object_name = 'homes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Расчет тепловой мощности по зданиям'
        context['total_heat_energy'] = total_heat_energy()
        return context


class CreateHome(CreateView):
    form_class = AddHomeForm
    template_name = 'thermo/create_home_power.html'
    success_url = reverse_lazy('heat_power_home')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UpdateHome(UpdateView):
    model = Home
    form_class = AddHomeForm
    template_name = 'thermo/create_home_power.html'
    success_url = reverse_lazy('heat_power_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DeleteHome(DeleteView):
    model = Home
    template_name = 'thermo/result_claculations.html'
    success_url = reverse_lazy('heat_power_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        """Переопределяем post, чтобы сразу удалять без подтверждения"""
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)
