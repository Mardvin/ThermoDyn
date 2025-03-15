import json

from django.views.generic import ListView, TemplateView

from heat_losses_app.functions.heat_insulations.main_heat_insulations import main_heat_insulation
from heat_losses_app.functions.heat_loss.main_heat_losses import main_heat_losses

# menu = [
#     {'title': "О сайте", 'url_name': 'about'},
#     {'title': "Добавить статью", 'url_name': 'add_data_about_home'},
#     {'title': "Войти", 'url_name': 'login'},
# ]

class ResultLosses(TemplateView):
    template_name = 'heat_losses_app/result_losses.html'

    def get_context_data(self, **kwargs):
        year_insulation = main_heat_insulation.heat_insulation.year_insulation
        calculate_utilized_heat = main_heat_losses.average_annual_temperature_networks.utilized_heat
        cost_filling_heat = main_heat_losses.average_annual_temperature_networks.cost_heat_fillup
        total = round(year_insulation + cost_filling_heat + calculate_utilized_heat, 2)

        data = {
            "labels": ["Заполнение трубопровода", "Утечки", "Через изоляцию"],
            "values": [cost_filling_heat, calculate_utilized_heat, year_insulation]
        }


        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['year_insulation'] = year_insulation
        context['calculate_utilized_heat'] = calculate_utilized_heat
        context['cost_filling_heat'] = cost_filling_heat
        context['total'] = total
        context['chart_data'] = json.dumps(data)


        return context