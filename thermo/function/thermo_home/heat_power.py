from decimal import Decimal, getcontext
from django.db.models import Sum


def calculate_heat_energy(
        heating_characteristic,
        building_volume,
        indoor_temperature,
        heating_duration_hours=Decimal("5400"),
        heat_loss_coefficient=Decimal("1.0"),
        regional_coefficient=Decimal("1.05"),
        outdoor_min_temperature=Decimal("-32")
):
    """
    Вычисляет количество теплоты, необходимое для отопления здания.

    :param heating_characteristic: Удельная отопительная характеристика здания (ккал/(м³·ч·°C))
    :param building_volume: Общий объем здания (м³)
    :param indoor_temperature: Средняя температура воздуха внутри здания (°C)
    :param heating_duration_hours: Продолжительность отопительного периода (часы)
    :param heat_loss_coefficient: Коэффициент учета потерь тепла (по умолчанию 1.0)
    :param regional_coefficient: Региональный коэффициент поправки (по умолчанию 1.05)
    :param outdoor_min_temperature: Минимальная температура наружного воздуха (°C, по умолчанию -32)

    :return: Количество теплоты в Гкал
    """
    getcontext().prec = 28  # Устанавливаем точность

    heating_characteristic = Decimal(str(heating_characteristic))
    building_volume = Decimal(str(building_volume))
    indoor_temperature = Decimal(str(indoor_temperature))
    heating_duration_hours = Decimal(str(heating_duration_hours))

    heat_energy = (
            Decimal("1")  # Коэффициент a, равный 1
            * heating_characteristic
            * building_volume
            * (indoor_temperature - outdoor_min_temperature)
            * regional_coefficient
            * heat_loss_coefficient
            * heating_duration_hours
            * Decimal("1e-6") # Перевод в Гкал
    )
    return heat_energy.quantize(Decimal("0.01"))


def total_heat_energy():
    from thermo.models import Home
    """ Считает суммарное кол-во теплоты в год для отопления """
    total = Home.objects.aggregate(total=Sum('heat_energy'))['total']
    return round(total, 2) if total is not None else 0.00