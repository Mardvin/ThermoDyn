from django.db.models import QuerySet

from config import Config


class NetworkVolume:
    """
    Класс для расчёта объёма теплоносителя в трубопроводной сети.

    Атрибуты:
        pipes_standard (PipeStandard): Объект, содержащий стандартные параметры труб (диаметры, материалы и др.).
        pipeline_segments (PipelineSegment): Объект, содержащий сегменты трубопровода с их характеристиками.
        a (float): норма среднегодовой утечки теплоносителя (м³/ч×м³).
        total_volume_network (float): Общий объём теплоносителя в сети (результат вычислений).
        hourly_annual_coolant_leakage_norm (float): Норматив утечек теплоносителя в час и за год (результат вычислений).
    """

    def __init__(self, pipes_standard: QuerySet, pipeline_segments: QuerySet, conf: Config):
        self.__pipes_standard = pipes_standard
        self.__pipeline_segments = pipeline_segments
        self.a = conf.volume_network.norm_leakage_a

        #result:
        self.total_volume_network = self.__total_volume_network()
        self.hourly_annual_coolant_leakage_norm = self.__hourly_annual_coolant_leakage_norm()

    @staticmethod
    def __get_specific_volume(diameter, pipes_standard):
        """
        Возвращает удельный объем для заданного диаметра трубы.
        Если точного совпадения нет, выполняет линейную интерполяцию или экстраполяцию.
        """
        pipes = list(pipes_standard)  # Приводим к списку, если это QuerySet
        pipes.sort(key=lambda x: x.diameter)  # Сортируем по диаметру

        if not pipes:
            return None  # Если в БД нет данных, вернуть None

        if len(pipes) == 1:
            return pipes[0].specific_volume  # Если в БД только одна труба, берем ее значение

        # Проверяем, есть ли точное совпадение
        for pipe in pipes:
            if pipe.diameter == diameter:
                return pipe.specific_volume

        # Если диаметр меньше минимального, выполняем экстраполяцию
        if diameter < pipes[0].diameter and len(pipes) > 1:
            d1, v1 = pipes[0].diameter, pipes[0].specific_volume
            d2, v2 = pipes[1].diameter, pipes[1].specific_volume
        # Если диаметр больше максимального, выполняем экстраполяцию
        elif diameter > pipes[-1].diameter and len(pipes) > 1:
            d1, v1 = pipes[-2].diameter, pipes[-2].specific_volume
            d2, v2 = pipes[-1].diameter, pipes[-1].specific_volume
        else:
            # Ищем ближайшие две точки для интерполяции
            for i in range(len(pipes) - 1):
                if pipes[i].diameter < diameter < pipes[i + 1].diameter:
                    d1, v1 = pipes[i].diameter, pipes[i].specific_volume
                    d2, v2 = pipes[i + 1].diameter, pipes[i + 1].specific_volume
                    break
            else:
                return None  # Если не нашли подходящие точки

        # Линейная интерполяция/экстраполяция
        specific_volume = v1 + (diameter - d1) * ((v2 - v1) / (d2 - d1))
        return round(specific_volume, 3)

    def __total_volume_network(self) -> float:
        """
        Расчет емкости трубопровода системы теплоснабжения
        """
        total_volume = 0
        pipelines_diam_len = [
            {"diameter": segment.diameter, "length": segment.length} for segment in self.__pipeline_segments
        ]

        for pipe in pipelines_diam_len:
            pipe_volume = self.__get_specific_volume(pipe["diameter"], self.__pipes_standard)
            if pipe_volume is not None:  # Проверяем, что значение не None
                total_volume += pipe_volume * 2 * pipe["length"]

        return round(total_volume, 3)

    def __hourly_annual_coolant_leakage_norm(self) -> float:
        """
        Cреднечасовая годовая норма потерь теплоносителя, обусловленных утечкой
        """
        result = self.a * self.total_volume_network / 100
        return round(result, 3)
