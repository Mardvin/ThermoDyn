from django.db import models
import math

from heat_losses_app.functions.heat_flux import calculate_heat_flux
from heat_losses_app.functions.main_heat_losses import main_heat_losses
from heat_losses_app.models.models import PipelineSegment


# Новая модель для учета коэффициента b и расчета теплопотерь
class HeatLossInsulation(models.Model):
    pipeline_segment = models.ForeignKey(PipelineSegment, on_delete=models.CASCADE)

    # Поле для коэфициента b, рассчитываемого на основе диаметра трубы
    b = models.FloatField(verbose_name="Коэффициент b")

    insulation_thickness_mm = models.FloatField(verbose_name="Толщина слоя теплоизоляционного материала (мм)")

    # Удельные часовые теплопотери для температуры воды в подающем трубопроводе
    heat_loss_supply = models.FloatField(verbose_name="Удельные теплопотери (поддающий трубопровод) ккал/(м·ч)",)

    # Удельные часовые теплопотери для температуры воды в обратном трубопроводе
    heat_loss_return = models.FloatField(verbose_name="Удельные теплопотери (обратный трубопровод) ккал/(м·ч)",)

    # Метод для вычисления коэффициента b
    def calculate_b(self):
        if self.pipeline_segment.diameter <= 150:
            self.b = 1.2
        else:
            self.b = 1.15

    # Метод для расчета удельных теплопотерь
    def calculate_heat_losses(self):
        """
        Рассчитывает удельные часовые теплопотери для подающего и обратного трубопроводов.
        """
        # Расчёт теплопотерь для подающего трубопровода
        self.heat_loss_supply = calculate_heat_flux(
            material_type=self.pipeline_segment.insulation_material,
            d_mm=self.pipeline_segment.diameter,
            insulation_thickness_mm=self.insulation_thickness_mm,
            t1=main_heat_losses.average_annual_temperature_networks.supply_network,
            pipe_laying_type=self.pipeline_segment.laying_type
        )

        # Расчёт теплопотерь для обратного трубопровода
        self.heat_loss_return = calculate_heat_flux(
            material_type=self.pipeline_segment.insulation_material,
            d_mm=self.pipeline_segment.diameter,
            insulation_thickness_mm=self.insulation_thickness_mm,
            t1=main_heat_losses.average_annual_temperature_networks.return_network,
            pipe_laying_type=self.pipeline_segment.laying_type
        )


    def save(self, *args, **kwargs):
        # Рассчитываем коэффициент b перед сохранением
        self.calculate_b()
        self.calculate_heat_losses()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Теплопотери для {self.pipeline_segment.diameter} мм, b={self.b}"