from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from heat_losses_app.forms import AddPipeLineSegment
from heat_losses_app.functions.main_heat_losses import DataRepository, main_heat_losses
from heat_losses_app.models.models import PipelineSegment

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
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['menu'] = menu
        context['network_volume'] = main_heat_losses.network_volume.total_volume_network
        context['network_leakage'] = main_heat_losses.network_leakage.leakage_loss
        context['segments'] = DataRepository.get_all_segments()
        context['temperature_graph'] = DataRepository.get_temperature_graph()
        context['temperature_supply'] = main_heat_losses.average_annual_temperature_networks.supply_network
        context['temperature_return'] = main_heat_losses.average_annual_temperature_networks.return_network
        context['hourly_annual_coolant_leakage'] = main_heat_losses.network_volume.hourly_annual_coolant_leakage_norm
        context['calculate_utilized_heat'] = main_heat_losses.average_annual_temperature_networks.utilized_heat
        context['cost_filling_heat'] = main_heat_losses.average_annual_temperature_networks.cost_heat_fillup
        return context


class CreatePipelineSegment(CreateView):
    form_class = AddPipeLineSegment
    template_name = 'heat_losses_app/create_pipeline_segment.html'
    success_url = reverse_lazy('heat_losses')

    def form_valid(self, form):
        form.save()
        main_heat_losses.update_result()
        return super().form_valid(form)


class UpdatePipeline(UpdateView):
    model = PipelineSegment
    form_class = AddPipeLineSegment
    template_name = 'heat_losses_app/create_pipeline_segment.html'
    success_url = reverse_lazy('heat_losses')

    def form_valid(self, form):
        response = super().form_valid(form)
        main_heat_losses.update_result()
        return response


class DeletePipeline(DeleteView):
    model = PipelineSegment
    template_name = 'heat_losses_app/heat_losses.html'
    success_url = reverse_lazy('heat_losses')

    def post(self, request, *args, **kwargs):
        """Переопределяем post, чтобы сразу удалять без подтверждения"""
        self.object = self.get_object()
        self.object.delete()
        main_heat_losses.update_result()
        return redirect(self.success_url)
