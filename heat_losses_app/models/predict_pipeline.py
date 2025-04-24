from django.db import models

from heat_losses_app.functions.heat_insulations.heat_flux import calculate_heat_flux
from heat_losses_app.functions.heat_loss.main_heat_losses import main_heat_losses
from heat_losses_app.functions.prediction.prediciton_models import predict_pipeline_replacement
from heat_losses_app.models import HeatLossInsulation


class PredictPipelineManager(models.Manager):
    def update_or_create_for_all_heat_loss_insulations(self):
        heat_loss_insulations = HeatLossInsulation.objects.all()

        for heat_loss in heat_loss_insulations:
            # Ищем, есть ли уже PredictPipline для данного участка
            obj, created = self.update_or_create(
                pipeline_segment_loss=heat_loss,  # Уникальный ключ
                defaults={
                    "new_insulation_material": "Пенополиуретан",  # Можно поменять логику
                    "replacement": predict_pipeline_replacement(
                        length=heat_loss.pipeline_segment.length,
                        diameter=heat_loss.pipeline_segment.diameter,
                        installation_type=heat_loss.pipeline_segment.laying_type,
                        insulation_material="Пенополиуретан",
                        year_of_operation=heat_loss.pipeline_segment.commissioning_year,
                    ),
                    "heat_loss_supply": calculate_heat_flux(
                        material_type="Пенополиуретан",
                        d_mm=heat_loss.pipeline_segment.diameter,
                        insulation_thickness_mm=heat_loss.insulation_thickness_mm,
                        t1=main_heat_losses.average_annual_temperature_networks.supply_network,
                        pipe_laying_type=heat_loss.pipeline_segment.laying_type
                    ),
                    "heat_loss_return": calculate_heat_flux(
                        material_type="Пенополиуретан",
                        d_mm=heat_loss.pipeline_segment.diameter,
                        insulation_thickness_mm=heat_loss.insulation_thickness_mm,
                        t1=main_heat_losses.average_annual_temperature_networks.return_network,
                        pipe_laying_type=heat_loss.pipeline_segment.laying_type
                    )
                }
            )

            # Пересчитываем годовые потери после создания/обновления
            obj.calculate_heat_loss_year()
            obj.save()  # Сохраняем

            action = "Создан" if created else "Обновлён"
            print(f"{action}: {obj}")


class PredictPipline(models.Model):
    pipeline_segment_loss = models.ForeignKey(HeatLossInsulation, on_delete=models.CASCADE)
    new_insulation_material = models.CharField(
        max_length=50,
        choices=[("Пенополиуретан", "Пенополиуретан")],
        default="Пенополиуретан",
        verbose_name="Новый теплоизоляционный материал",
    )
    replacement = models.CharField(max_length=3, choices=[("Да", "Да"), ("Нет", "Нет")], verbose_name="Замена "
                                                                                                      "трубопровода")
    heat_loss_supply = models.FloatField(verbose_name="Удельные теплопотери (поддающий трубопровод) ккал/(м·ч)",)
    heat_loss_return = models.FloatField(verbose_name="Удельные теплопотери (обратный трубопровод) ккал/(м·ч)",)
    heat_loss_year = models.FloatField(verbose_name="Годовые нормы тепловых потерь Гкал")

    objects = PredictPipelineManager()

    def get_replacement(self):
        self.replacement=predict_pipeline_replacement(
            length=self.pipeline_segment_loss.pipeline_segment.length,
            diameter=self.pipeline_segment_loss.pipeline_segment.diameter,
            installation_type=self.pipeline_segment_loss.pipeline_segment.laying_type,
            insulation_material=self.new_insulation_material,
            year_of_operation=self.pipeline_segment_loss.pipeline_segment.commissioning_year,
        )

    def calculate_heat_losses(self):
        """
        Рассчитывает удельные часовые теплопотери для подающего и обратного трубопроводов.
        """
        # Расчёт теплопотерь для подающего трубопровода
        self.heat_loss_supply = calculate_heat_flux(
            material_type=self.new_insulation_material,
            d_mm=self.pipeline_segment_loss.pipeline_segment.diameter,
            insulation_thickness_mm=self.pipeline_segment_loss.insulation_thickness_mm,
            t1=main_heat_losses.average_annual_temperature_networks.supply_network,
            pipe_laying_type=self.pipeline_segment_loss.pipeline_segment.laying_type
        )

        # Расчёт теплопотерь для обратного трубопровода
        self.heat_loss_return = calculate_heat_flux(
            material_type=self.new_insulation_material,
            d_mm=self.pipeline_segment_loss.pipeline_segment.diameter,
            insulation_thickness_mm=self.pipeline_segment_loss.insulation_thickness_mm,
            t1=main_heat_losses.average_annual_temperature_networks.return_network,
            pipe_laying_type=self.pipeline_segment_loss.pipeline_segment.laying_type
        )

    def calculate_heat_loss_year(self):
        self.heat_loss_year = round((
                                      self.heat_loss_supply * self.pipeline_segment_loss.b * self.pipeline_segment_loss.pipeline_segment.length
                                    ) + (
                                    self.heat_loss_return * self.pipeline_segment_loss.b * self.pipeline_segment_loss.pipeline_segment.length
        ) * 1e-6, 2)

    def save(self, *args, **kwargs):
        # Рассчитываем перед сохранением
        self.get_replacement()
        self.calculate_heat_losses()
        self.calculate_heat_loss_year()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"замена трубопровода {self.replacement}"

