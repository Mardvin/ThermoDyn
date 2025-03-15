from django.db import models

class BoilerRoomPump(models.Model):
    PUMP_TYPES = [
        ('подпиточный', 'Подпиточный'),
        ('сетевой', 'Сетевой'),
    ]

    pump_type = models.CharField(max_length=50, verbose_name='Модель насоса')  # Например, "К 20/30"
    pump_category = models.CharField(max_length=20, choices=PUMP_TYPES, verbose_name='Вид насоса')  # Вид насоса
    power_kW = models.FloatField(verbose_name='Мощность двигателя')  # Мощность двигателя, кВт
    operating_hours = models.PositiveIntegerField(verbose_name='Продолжительность работы')  # Продолжительность # работы, ч

    def __str__(self):
        return f"{self.pump_type} ({self.pump_category}) - {self.power_kW} кВт"