from collections import defaultdict

from heat_losses_app.models import HeatLossInsulation
from heat_losses_app.models.models import PipelineSegment


class HeatLossCalculator:
    LAYING_TYPE_MAP = {
        "Наземная прокладка": "above_ground",
        "Подземная прокладка": "underground",
        "В канале": "channel",
    }

    def __init__(self):
        """
        Инициализация калькулятора теплопотерь.
        `heat_loss_by_laying_type` хранит сумму потерь по каждому типу прокладки + общий итог.
        """
        # Инициализация словаря с нулями для каждого типа прокладки и общего итога
        self.heat_loss_by_laying = self.calculate_heat_loss()
        self.result_insulation = self.get_results()

    def calculate_heat_loss(self):
        """
        Рассчитывает суммарные часовые теплопотери для каждого типа прокладки.
        """
        heat_loss_by_laying_type = {
            "above_ground": 0,
            "underground": 0,
            "channel": 0,
            "total": 0
        }
        pipeline_segments = PipelineSegment.objects.all()

        for segment in pipeline_segments:
            heat_loss_insulation = HeatLossInsulation.objects.filter(pipeline_segment=segment).first()

            if not heat_loss_insulation:
                continue  # Если данных по теплоизоляции нет, пропускаем сегмент

            # Длина участка в метрах (перевод из км в м)
            length_m = segment.length * 1000

            # Расчет теплопотерь для подающего и обратного трубопровода
            total_heat_loss_kcal_per_hour = (
                heat_loss_insulation.heat_loss_supply * length_m * heat_loss_insulation.b +
                heat_loss_insulation.heat_loss_return * length_m * heat_loss_insulation.b
            )

            # Перевод в Гкал/ч
            total_heat_loss_gcal_per_hour = total_heat_loss_kcal_per_hour * 1e-6

            # Переводим тип прокладки в английское название
            laying_type = self.LAYING_TYPE_MAP.get(segment.laying_type)

            if laying_type:
                # Сохраняем сумму теплопотерь по типу прокладки
                heat_loss_by_laying_type[laying_type] += total_heat_loss_gcal_per_hour

                # Добавляем в общий итог
                heat_loss_by_laying_type["total"] += total_heat_loss_gcal_per_hour
        return heat_loss_by_laying_type

    def get_results(self):
        """
        Возвращает словарь с теплопотерями по каждому типу прокладки + общий итог (округленные значения).
        """
        return {key: round(value, 5) for key, value in self.heat_loss_by_laying.items()}