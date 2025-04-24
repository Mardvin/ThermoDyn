from config import load_config
from core.db import DataRepository
from heat_losses_app.functions.heat_insulations.insulation_losses import HeatLossCalculator


config = load_config()


class MainHeatInsulations():
    def __init__(self):
        """Создаём объект с новыми данными"""
        self.heat_insulation = HeatLossCalculator(
            conf=config,
            pipeline_segments=DataRepository.get_all_segments()
        )

    def update_result(self):
        self.heat_insulation = HeatLossCalculator(
            conf=config,
            pipeline_segments=DataRepository.get_all_segments()
        )


main_heat_insulation = MainHeatInsulations()


