from enum import Enum
from typing import Dict

from pydantic import BaseModel


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