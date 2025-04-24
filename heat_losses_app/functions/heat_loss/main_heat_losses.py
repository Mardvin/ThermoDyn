from config import load_config
from core.db import DataRepository
from heat_losses_app.functions.heat_loss.heat_loss_leakage import NetworkLeakage
from heat_losses_app.functions.heat_loss.network_volume import NetworkVolume
from heat_losses_app.functions.heat_loss.temperature_analysis import TemperatureCalculator


config = load_config()


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
