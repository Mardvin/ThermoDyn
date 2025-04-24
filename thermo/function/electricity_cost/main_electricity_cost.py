from config import load_config
from core.db import DataRepository
from thermo.function.electricity_cost.electricity_result import ElectricityResult

config = load_config()


class MainElectricityCost(DataRepository):
    def __init__(self):
        """Создаём объект с новыми данными"""
        self.electricity = ElectricityResult(
            boilers_room_pump=DataRepository.get_electricity_machine()
        )

    def update_result(self):
        self.electricity = ElectricityResult(
            boilers_room_pump=DataRepository.get_electricity_machine()
        )


main_electricity_cost = MainElectricityCost()
