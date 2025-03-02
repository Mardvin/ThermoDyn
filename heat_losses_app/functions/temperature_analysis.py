# from django.db.models import Avg
from django.db.models import QuerySet

from config import Config
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

    def __init__(self, conf: Config, annual_coolant_leakage_norm: float):
        self.__temperature_graph = TemperatureGraph.objects.values(
            "pipe_type", *MONTH_DAYS.keys()
        )
        self.__temperature_graph_supply_return = self.__get_temperature_data()
        self.__heating_hours = conf.general.heating_hours
        self.__hourly_annual_coolant_leakage_norm = annual_coolant_leakage_norm
        self.__conf = conf
         # Возвращает:
        self.supply_network = self.__calculate_yearly_temperature('supply')
        self.return_network = self.__calculate_yearly_temperature('return')
        self.utilized_heat = self.__calculate_utilized_heat()

    def __get_temperature_data(self):
        """
        Получает данные из модели TemperatureGraph и возвращает
        словарь:
        {
            "supply": { "january": 70, "february": 65, ... },
            "return": { "january": 50, "february": 45, ... }
        }
        """
        result = {"supply": {}, "return": {}}

        for entry in self.__temperature_graph:
            pipe_type = "supply" if entry["pipe_type"] == "Подающий" else "return"
            for month in TemperatureCalculator.MONTH_MAPPING:
                result[pipe_type][month] = entry[month]

        return result

    def __calculate_yearly_temperature(self, pipe_type: str) -> float:
        """
        Вычисляет среднегодовую температуру для указанного трубопровода.
        :param pipe_type: "supply" или "return"
        :return: Среднегодовая температура
        """
        if pipe_type not in self.__temperature_graph_supply_return:
            return 0

        total_sum = sum(
            self.__temperature_graph_supply_return[pipe_type][month] * MONTH_DAYS[month] * 24
            for month in MONTH_DAYS
            if month in self.__temperature_graph_supply_return[pipe_type]
        )
        return round(total_sum / self.__heating_hours if self.__heating_hours else 0, 2)

    def __calculate_utilized_heat(self) -> float:
        """
        Вычисляет нормативное значение годовых технологических тепловых потерь с утечкой

        :return: Технологичкие потери с утечкой (Гкал)
        """
        density_water = self.__conf.general.density_water
        specific_heat = self.__conf.general.specific_heat
        temp_distribution_coeff = self.__conf.general.temp_distribution_coeff
        temp_water_supplementation = self.__conf.temperature.temp_water_supplementation
        heating_hours = self.__conf.general.heating_hours

        utilized_heat = (
                                self.__hourly_annual_coolant_leakage_norm * density_water * specific_heat *
                                (temp_distribution_coeff * self.supply_network + (1 - temp_distribution_coeff)
                                 * self.return_network - temp_water_supplementation) * heating_hours
                        ) * 10 ** -6
        return round(utilized_heat, 2)
