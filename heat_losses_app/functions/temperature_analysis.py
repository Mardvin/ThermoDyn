# from django.db.models import Avg
from heat_losses_app.models import TemperatureGraph

MONTH_DAYS = {
    "january": 31,
    "february": 28,
    "march": 31,
    "april": 3,
    "may": 31,
    "june": 30,
    "july": 31,
    "august": 31,
    "september": 30,
    "october": 31,
    "november": 30,
    "december": 31,
}


class TemperatureCalculator:
    """Класс для расчёта годовой температуры теплоносителя."""

    MONTH_MAPPING = {month: month for month in MONTH_DAYS}  # Маппинг месяцев

    def __init__(self):
        """Инициализация без данных — они берутся из БД."""
        self.data = self.get_temperature_data()  # Загружаем данные при создании объекта

    @staticmethod
    def get_temperature_data():
        """
        Получает данные из модели TemperatureGraph и возвращает
        словарь:
        {
            "supply": { "january": 70, "february": 65, ... },
            "return": { "january": 50, "february": 45, ... }
        }
        """
        data = TemperatureGraph.objects.values(
            "pipe_type", *MONTH_DAYS.keys()
        )

        result = {"supply": {}, "return": {}}

        for entry in data:
            pipe_type = "supply" if entry["pipe_type"] == "Подающий" else "return"
            for month in TemperatureCalculator.MONTH_MAPPING:
                result[pipe_type][month] = entry[month]

        return result

    def calculate_yearly_temperature(self, pipe_type: str) -> float:
        """
        Вычисляет среднегодовую температуру для указанного трубопровода.
        :param pipe_type: "supply" или "return"
        :return: Среднегодовая температура
        """
        if pipe_type not in self.data:
            return 0

        total_hours = 5160
        total_sum = sum(
            self.data[pipe_type][month] * MONTH_DAYS[month] * 24
            for month in MONTH_DAYS
            if month in self.data[pipe_type]
        )

        return round(total_sum / total_hours if total_hours else 0, 2)

    def result(self):
        return {'supply': self.calculate_yearly_temperature('supply'), 'return': self.calculate_yearly_temperature('return')}


def calculate_utilized_heat(temp_stage1, temp_stage2,):
    """
    Вычисляет количество утилизируемого тепла Q_у.н. по заданной формуле.

    :param mass_per_year: среднечасовая годовая норма потерь теплоносителя, обусловленных утечкой (кг)
    :param density: Плотность теплоносителя (кг/м³)
    :param specific_heat: Удельная теплоёмкость (Дж/(кг·°C))
    :param temp_distribution_coeff: Коэффициент распределения температур (безразмерный)
    :param temp_stage1: Температура первой стадии (°C)
    :param temp_stage2: Температура второй стадии (°C)
    :param ambient_temp: Температура окружающей среды (°C)
    :param heat_utilization_coeff: отопительный период ч
    :return: Утилизируемое тепло (Гкал)
    """
    mass_per_year = 0.15  # Например, 1000 кг
    density = 1000  # Плотность воды 1000 кг/м³
    specific_heat = 1  # удельная теплоемкость теплоносителя (ккал/(кг·°C))
    temp_distribution_coeff = 0.75  # Например, 0.5
    ambient_temp = 5  # Температура холодной воды подпитки (°C)
    heat_utilization_coeff = 5160  # Отопительный период

    utilized_heat = (
        mass_per_year * density * specific_heat *
        (temp_distribution_coeff * temp_stage1 + (1 - temp_distribution_coeff) * temp_stage2 - ambient_temp) *
        heat_utilization_coeff
    ) * 10**-6
    return round(utilized_heat, 2)

