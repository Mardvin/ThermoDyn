class VolumeLossLeakage:
    def __init__(self,
                 pipeline_capacity: float,
                 leakage_rate: float = 0.25,
                 heating_hours: int = 5160,
                 summer_hours: int = 0
                 ):
        """
        Класс для расчета годовых потерь теплоносителя утечкой.

        :param pipeline_capacity: Объем теплоносителя в трубопроводе в отопительный период (м³)
        :param leakage_rate: Норма утечки теплоносителя (в %, по умолчанию 0.25%)
        :param heating_hours: Количество часов отопительного периода (по умолчанию 5160 часов = 215 дней)
        :param summer_hours: Количество часов летнего периода (по умолчанию 0)
        """
        self.pipeline_capacity = pipeline_capacity  # Объем теплоносителя в трубопроводе в отопительный период
        self.leakage_rate = leakage_rate  # Норма утечки теплоносителя в процентах
        self.heating_hours = heating_hours  # Часы отопительного периода
        self.summer_hours = summer_hours  # Часы летнего периода
        self.total_hours = self.heating_hours + self.summer_hours  # Общее количество часов работы теплоснабжения за год

        # Рассчитываем потери при создании объекта
        self.leakage_loss = self.__calculate_annual_leakage_loss()

    def __calculate_average_annual_capacity(self) -> float:
        """
        Вычисляет среднегодовую емкость теплоносителя в сети теплоснабжения.

        :return: Среднегодовая емкость (м³)
        """
        return round(self.pipeline_capacity * self.heating_hours / self.total_hours, 3)

    def __calculate_annual_leakage_loss(self) -> float:
        """
        Вычисляет годовые потери теплоносителя из-за утечек.

        :return: Годовые потери теплоносителя (м³)
        """
        average_annual_capacity = self.__calculate_average_annual_capacity()
        annual_leakage_loss = (self.leakage_rate / 100) * average_annual_capacity * self.total_hours
        return round(annual_leakage_loss, 3)

    def __float__(self):
        """
        Позволяет получать значение утечек при преобразовании объекта в float.
        """
        return self.leakage_loss
