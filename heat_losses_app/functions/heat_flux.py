import math

from config import Config, load_config
from heat_losses_app.models import InsulationMaterial, HeatTransferCoefficient

config = load_config()


def get_environment_temperature(pipe_laying_type: str, config: Config) -> int:
    """
    Возвращает температуру окружающей среды в зависимости от типа прокладки.

    :param pipe_laying_type: Тип прокладки (Underground, Aboveground, In channel).
    :param config: Конфигурация с температурными значениями.
    :return: Температура окружающей среды (°C).
    """
    temperature_mapping = {
        "Подземная прокладка": config.temperature.temp_underground,
        "Наземная прокладка": config.temperature.temp_aboveground,
        "В канале": config.temperature.temp_in_channel,
    }

    return temperature_mapping.get(pipe_laying_type)


def calculate_heat_flux(material_type, d_mm, insulation_thickness_mm, t1, pipe_laying_type):
    """
    Рассчитывает линейную плотность теплового потока q.

    :param material_type: Вид материала изоляции (название из модели).
    :param d_mm: Наружный диаметр трубы (мм).
    :param insulation_thickness_mm: Толщина изоляции (мм).
    :param t1: Температура теплоносителя (°С).
    :param t2: Температура внешней среды (°С).
    :param pipe_laying_type: Тип прокладки трубы ("Подземная", "Наземная", "В канале").
    :return: Линейная плотность теплового потока q (Вт/м) и (ккал/(м·ч)).
    """
    try:
        # Получаем теплопроводность изоляции из модели
        insulation = InsulationMaterial.objects.get(name=material_type)
        lambda_u = insulation.thermal_conductivity  # Вт/(м·°С)
        print(pipe_laying_type)
        t2 = get_environment_temperature(pipe_laying_type, config)

        # Получаем коэффициенты теплоотдачи
        alpha1 = HeatTransferCoefficient.objects.get(environment="Вода в трубе").alpha  # Внутри трубы
        alpha2 = HeatTransferCoefficient.objects.get(environment=pipe_laying_type).alpha  # Внешний коэффициент
    except (InsulationMaterial.DoesNotExist, HeatTransferCoefficient.DoesNotExist):
        raise ValueError("Ошибка: Материал изоляции или коэффициент теплоотдачи не найден в базе данных")

    # Перевод диаметра и толщины изоляции из мм в метры
    d = d_mm / 1000  # наружный диаметр трубы, м
    insulation_thickness = insulation_thickness_mm / 1000  # толщина изоляции, м
    d_u = d + 2 * insulation_thickness  # наружный диаметр изоляции, м

    # Проверка на корректность входных данных
    if d <= 0 or d_u <= d or lambda_u <= 0 or alpha1 <= 0 or alpha2 <= 0:
        raise ValueError("Некорректные входные параметры")

    # Вычисление q в Вт/м
    numerator = math.pi * (t1 - t2)
    denominator = (1 / (alpha1 * d)) + (1 / (2 * lambda_u) * math.log(d_u / d)) + (1 / (alpha2 * d_u))
    q_watt_per_meter = numerator / denominator

    # Перевод в ккал/(м·ч)
    q_kcal_per_meter_hour = q_watt_per_meter * 0.8598

    return round(q_kcal_per_meter_hour, 2)