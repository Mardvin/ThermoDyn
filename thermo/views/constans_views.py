from django.shortcuts import render
from config import load_config

def about_project_view(request):
    return render(request, "thermo/about_project.html")


def constants_view(request):
    config = load_config()

    context = {
        "general": [
            {"name": "Часы отопительного периода", "key": "heating_hours", "value": config.general.heating_hours,
             "description": "Количество часов отопительного периода"},
            {"name": "Часы летнего периода", "key": "heating_summer_hours",
             "value": config.general.heating_summer_hours, "description": "Количество часов летнего периода"},
            {"name": "Плотность воды", "key": "density_water", "value": config.general.density_water,
             "description": "Плотность воды (кг/м³)"},
            {"name": "Удельная теплоемкость", "key": "specific_heat", "value": config.general.specific_heat,
             "description": "Удельная теплоемкость теплоносителя (ккал/(кг·°C))"},
            {"name": "Коэффициент распределения тепла", "key": "temp_distribution_coeff",
             "value": config.general.temp_distribution_coeff,
             "description": "Доля массового расхода теплоносителя, теряемого подающим трубопроводом"},
        ],
        "temperature": [
            {"name": "Температура окружающей среды", "key": "temp_water_supplementation",
             "value": config.temperature.temp_water_supplementation,
             "description": "Температура окружающей среды (°C)"},
            {"name": "Температура воды для заполнения", "key": "temp_fill_water",
             "value": config.temperature.temp_fill_water,
             "description": "Температура воды, используемой для заполнения трубопровода (°C)"},
            {"name": "Температура грунта", "key": "temp_underground", "value": config.temperature.temp_underground,
             "description": "Температура грунта (°C)"},
            {"name": "Температура воздуха", "key": "temp_aboveground", "value": config.temperature.temp_aboveground,
             "description": "Температура воздуха (°C)"},
            {"name": "Температура в канале", "key": "temp_in_channel", "value": config.temperature.temp_in_channel,
             "description": "Температура в канале (°C)"},
        ],
        "volume_network": [
            {"name": "Норма утечки теплоносителя", "key": "norm_leakage_a",
             "value": config.volume_network.norm_leakage_a,
             "description": "Норма среднегодовой утечки теплоносителя (м³/ч×м³)"},
        ],
    }

    return render(request, "thermo/constants_page.html", {"sections": context})