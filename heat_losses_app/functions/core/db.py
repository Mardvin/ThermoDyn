from django.db.models import QuerySet

# from heat_losses_app.models import HeatLossInsulation
from heat_losses_app.models.models import PipelineSegment, PipeStandard, TemperatureGraph


class DataRepository:
    """
    Универсальный репозиторий для работы с базой данных.
    Позволяет получать данные из различных моделей Django.
    """

    @staticmethod
    def get_all_segments() -> QuerySet:
        """Получает все сегменты трубопровода."""
        return PipelineSegment.objects.all()

    @staticmethod
    def get_pipe_standards() -> QuerySet:
        """Получает все стандарты по трубам."""
        return PipeStandard.objects.all()

    @staticmethod
    def get_temperature_graph() -> QuerySet:
        return TemperatureGraph.objects.all()

    # @staticmethod
    # def get_insulation_losses() -> QuerySet:
    #     return HeatLossInsulation.objects.all()