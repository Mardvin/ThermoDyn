from config import Config


class LeakageNetwork:
    def __init__(self, volume_pipelines: float, conf: Config):
        """
        Класс для расчета годовых потерь теплоносителя утечкой.
        :param volume_pipelines: Объем теплоносителя в трубопроводе в отопительный период (м³)
        :param heating_hours: Количество часов отопительного периода (по умолчанию 5160 часов = 215 дней)
        :param summer_hours: Количество часов летнего периода (по умолчанию 0)
        """
        self.__pipeline_capacity = volume_pipelines  # Объем теплоносителя в трубопроводе в отопительный период
        self.__norm_leakage_a = conf.volume_network.norm_leakage_a
        self.__heating_hours = conf.general.heating_hours
        self.__summer_hours = conf.general.heating_summer_hours
        self.__total_hours = self.__heating_hours + self.__summer_hours  # Общее количество часов работы
        # теплоснабжения за год

        # годовые потери теплоносителя из-за утечек
        self.leakage_loss = self.__calculate_annual_leakage_loss()

    def __calculate_average_annual_capacity(self) -> float:
        """
        Вычисляет среднегодовую емкость теплоносителя в сети теплоснабжения.

        :return: Среднегодовая емкость (м³)
        """
        return round(self.__pipeline_capacity * self.__heating_hours / self.__total_hours, 3)

    def __calculate_annual_leakage_loss(self) -> float:
        """
        Вычисляет годовые потери теплоносителя из-за утечек.

        :return: Годовые потери теплоносителя (м³)
        """
        average_annual_capacity = self.__calculate_average_annual_capacity()
        annual_leakage_loss = (self.__norm_leakage_a / 100) * average_annual_capacity * self.__total_hours
        return round(annual_leakage_loss, 3)