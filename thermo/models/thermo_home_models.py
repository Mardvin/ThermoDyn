from django.db import models

from thermo.function.heat_power import calculate_heat_energy


class Home(models.Model):
    street_name = models.CharField(max_length=255, verbose_name='Улица')
    numbers = models.IntegerField(verbose_name='Номер дома')
    construction_volume = models.IntegerField(verbose_name='Строительный объем')
    indoor_air_temperature = models.IntegerField(default=20, verbose_name='Внутренняя температура воздуха') # todo подумать над выбором между образовательным и жилым
    construction_year = models.IntegerField(verbose_name='Год постройки') # todo поменять на выбор между двумя значениями
    heating_characteristic = models.FloatField(verbose_name='Удельная отопительная характеристика', editable=False)
    heat_energy = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Тепловая энергия", editable=False
    )

    def save(self, *args, **kwargs):
        # Рассчитать heating_characteristic перед сохранением
        self.heating_characteristic = self.get_heating_characteristic()
        self.heat_energy = calculate_heat_energy(
            heating_characteristic=self.heating_characteristic,
            building_volume=self.construction_volume,
            indoor_temperature=self.indoor_air_temperature
        )
        super().save(*args, **kwargs)

    def get_heating_characteristic(self):
        # Таблица значений: (объем, характеристика до 1958 года, характеристика после 1958 года)
        characteristics = [
            (100, 0.74, 0.92),
            (200, 0.66, 0.82),
            (300, 0.62, 0.78),
            (400, 0.6,  0.75),
            (500, 0.58, 0.73),
            (600, 0.55, 0.7),
            (700, 0.53, 0.68),
            (800, 0.51, 0.66),
            (900, 0.49, 0.64),
            (1000, 0.47, 0.62),
            (1500, 0.42, 0.57),
            (2000, 0.39, 0.54),
            (3000, 0.36, 0.5),
            (5000, 0.34, 0.47),
            (10000, 0.33, 0.44),
            (20000, 0.32, 0.43),
            (30000, 0.31, 0.42),
            (50000, 0.3,  0.41),
        ]

        # Определение года постройки
        year_built = self.construction_year

        # Выбор колонки характеристик в зависимости от года постройки
        if year_built <= 1958:
            column = 1  # Используем значения до 1958 года
        else:
            column = 2  # Используем значения после 1958 года

        # Подбор значения в зависимости от объема
        for volume, characteristic_before, characteristic_after in characteristics:
            if self.construction_volume <= volume:
                return characteristic_before if column == 1 else characteristic_after

        return None  # Возвращаем None, если значение не найдено

    def __str__(self):
        return f'{self.street_name}: {self.numbers}'

    class Meta:
        verbose_name = 'Параметры дома'
        verbose_name_plural = 'Параметры дома'
