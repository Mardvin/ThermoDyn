from django.db import models


class InsulationMaterial(models.Model):
    """Модель для хранения данных о материалах теплоизоляции"""
    name = models.CharField(max_length=255, unique=True, verbose_name="Вид материала")
    thermal_conductivity = models.FloatField(verbose_name="Теплопроводность, Вт/(м·°С)")

    def __str__(self):
        return f"{self.name} ({self.thermal_conductivity} Вт/(м·°С))"

    class Meta:
        verbose_name = "Материал изоляции"
        verbose_name_plural = "Материалы изоляции"


class HeatTransferCoefficient(models.Model):
    """
    Модель для хранения коэффициентов теплоотдачи для различных типов среды.
    """

    class EnvironmentType(models.TextChoices):
        WATER = "Вода в трубе", "Вода в трубе"
        UNDERGROUND = "Подземная прокладка", "Подземная прокладка"
        ABOVEGROUND = "Наземная прокладка", "Наземная прокладка"
        CHANNEL = "В канале", "В канале"

    environment = models.CharField(
        max_length=50,
        choices=EnvironmentType.choices,
        unique=True,
        verbose_name="Тип среды"
    )
    alpha = models.FloatField(verbose_name="Коэффициент теплоотдачи, Вт/(м²·°С)")

    def __str__(self):
        return f"{self.environment}: {self.alpha} Вт/(м²·°С)"

    class Meta:
        verbose_name = "Коэффициент теплоотдачи"
        verbose_name_plural = "Коэффициенты теплоотдачи"
