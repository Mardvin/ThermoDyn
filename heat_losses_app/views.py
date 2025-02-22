from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from heat_losses_app.forms import AddPipeLineSegment
from heat_losses_app.functions.heat_loss_leakage import VolumeLossLeakage
from heat_losses_app.functions.network_volume import total_volume_network, hourly_annual_coolant_leakage_norm
from heat_losses_app.functions.temperature_analysis import TemperatureCalculator
from heat_losses_app.models import PipelineSegment, TemperatureGraph

# Create your views here.

menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Добавить статью", 'url_name': 'add_data_about_home'},
    {'title': "Войти", 'url_name': 'login'},
]

class PipelineSegmentTable(ListView):
    model = PipelineSegment
    template_name = 'heat_losses_app/heat_losses.html'
    context_object_name = 'segments'

    def get_context_data(self, **kwargs):
        total_volume = total_volume_network()

        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['network_volume'] = total_volume
        context['volume_leakage'] = float(VolumeLossLeakage(pipeline_capacity=total_volume))
        context['segments'] = PipelineSegment.objects.all()
        context['temperature_graph'] = TemperatureGraph.objects.all()
        context['temperature_supply_return'] = TemperatureCalculator().result()
        context['hourly_annual_coolant_leakage'] = hourly_annual_coolant_leakage_norm()
        return context


class CreatePipelineSegment(CreateView):
    form_class = AddPipeLineSegment
    template_name = 'heat_losses_app/create_pipeline_segment.html'
    success_url = reverse_lazy('heat_losses')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class UpdatePipeline(UpdateView):
    model = PipelineSegment
    form_class = AddPipeLineSegment
    template_name = 'heat_losses_app/create_pipeline_segment.html'
    success_url = reverse_lazy('heat_losses')


class DeletePipeline(DeleteView):
    model = PipelineSegment
    template_name = 'heat_losses_app/heat_losses.html'
    success_url = reverse_lazy('heat_losses')

    def post(self, request, *args, **kwargs):
        """Переопределяем post, чтобы сразу удалять без подтверждения"""
        self.object = self.get_object()
        self.object.delete()
        return redirect(self.success_url)