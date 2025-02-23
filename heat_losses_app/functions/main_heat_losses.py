from django.db.models import QuerySet

from config import load_config
from heat_losses_app.functions.network_volume import NetworkVolume
from heat_losses_app.models import PipelineSegment, PipeStandard

config = load_config()


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
        """Получает все стандартные трубы."""
        return PipeStandard.objects.all()


class MainHeatLosses:
    network_volume = NetworkVolume(
        DataRepository.get_pipe_standards(),
        DataRepository.get_all_segments(),
        conf=config,
    )