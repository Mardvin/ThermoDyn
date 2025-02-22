from django.db import models

# Create your models here.

class LayingType(models.TextChoices):
    UNDERGROUND = "Подземная", "Подземная"
    ABOVEGROUND = "Наземная", "Наземная"
    CHANNEL = "В канале", "В канале"

class InsulationType(models.TextChoices):
    MINERAL_WOOL = "Минеральная вата", "Минеральная вата"
    POLYURETHANE = "Пенополиуретан", "Пенополиуретан"
    FOAMGLASS = "Пеностеклоs", "Пеностекло"
    NONE = "Без изоляции", "Без изоляции"


class PipelineSegment(models.Model):
    diameter = models.IntegerField(verbose_name="Диаметр трубы (мм)")
    length = models.FloatField(verbose_name="Длина участка (км)")
    insulation_material = models.CharField(
        max_length=50,
        choices=InsulationType.choices,
        verbose_name="Теплоизоляционный материал"
    )
    laying_type = models.CharField(
        max_length=20,
        choices=LayingType.choices,
        verbose_name="Тип прокладки"
    )
    commissioning_year = models.PositiveIntegerField(verbose_name="Год ввода в эксплуатацию")

    def __str__(self):
        return f"{self.diameter} мм, {self.length} м, {self.commissioning_year} г."



class PipeStandard(models.Model):
    """
    Удельный объем трубопровода тепловой сети
    СП 124.13330.2012 — свод правил «Тепловые сети. Актуализированная редакция СНиП 41-02-2003»
    """
    diameter = models.PositiveIntegerField(verbose_name="Диаметр трубы, мм", unique=True)
    specific_volume = models.FloatField(verbose_name="Удельный объем, куб. м/км")

    class Meta:
        verbose_name = "Стандартная труба"
        verbose_name_plural = "Стандартные трубы"
        ordering = ["diameter"]

    def __str__(self):
        return f"⌀{self.diameter} мм - {self.specific_volume} м³/км"


class TemperatureGraph(models.Model):
    PIPE_TYPE_CHOICES = [
        ('Подающий', 'Подающий'),
        ('Обратный', 'Обратный'),
    ]

    name = models.CharField(max_length=255, verbose_name="Наименование котельной")
    pipe_type = models.CharField(
        max_length=10, choices=PIPE_TYPE_CHOICES, verbose_name="Тип трубопровода"
    )

    # Температуры по месяцам
    january = models.IntegerField(default=0, verbose_name="Январь")
    february = models.IntegerField(default=0, verbose_name="Февраль")
    march = models.IntegerField(default=0, verbose_name="Март")
    april = models.IntegerField(default=0, verbose_name="Апрель")
    may = models.IntegerField(default=0, verbose_name="Май")
    june = models.IntegerField(default=0, verbose_name="Июнь")
    july = models.IntegerField(default=0, verbose_name="Июль")
    august = models.IntegerField(default=0, verbose_name="Август")
    september = models.IntegerField(default=0, verbose_name="Сентябрь")
    october = models.IntegerField(default=0, verbose_name="Октябрь")
    november = models.IntegerField(default=0, verbose_name="Ноябрь")
    december = models.IntegerField(default=0, verbose_name="Декабрь")

    class Meta:
        verbose_name = "Температурный график"
        verbose_name_plural = "Температурные графики"

    def __str__(self):
        return f"{self.name} ({self.get_pipe_type_display()})"
