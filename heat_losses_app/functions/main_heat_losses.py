from django.db.models import QuerySet

from config import load_config
from heat_losses_app.functions.heat_loss_leakage import NetworkLeakage
from heat_losses_app.functions.network_volume import NetworkVolume
from heat_losses_app.functions.temperature_analysis import TemperatureCalculator
from heat_losses_app.models.models import PipelineSegment, PipeStandard, TemperatureGraph

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
        """Получает все стандарты по трубам."""
        return PipeStandard.objects.all()

    @staticmethod
    def get_temperature_graph() -> QuerySet:
        return TemperatureGraph.objects.all()


class MainHeatLosses:
    def __init__(self):
        """Создаём объект с новыми данными"""
        self.network_volume = NetworkVolume(
            DataRepository.get_pipe_standards(),
            DataRepository.get_all_segments(),
            conf=config,
        )
        self.network_leakage = NetworkLeakage(
            self.network_volume.total_volume_network,
            conf=config,
        )
        self.average_annual_temperature_networks = TemperatureCalculator(
            conf = config,
            annual_coolant_leakage_norm=self.network_volume.hourly_annual_coolant_leakage_norm,
            volume_network = self.network_volume.total_volume_network,
        )

    def update_result(self):
        self.network_volume = NetworkVolume(
            DataRepository.get_pipe_standards(),
            DataRepository.get_all_segments(),
            conf=config,
        )
        self.network_leakage = NetworkLeakage(
            self.network_volume.total_volume_network,
            conf=config,
        )
        self.average_annual_temperature_networks = TemperatureCalculator(
            conf=config,
            annual_coolant_leakage_norm=self.network_volume.hourly_annual_coolant_leakage_norm,
            volume_network = self.network_volume.total_volume_network,
        )

main_heat_losses = MainHeatLosses()
