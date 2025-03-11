from heat_losses_app.functions.heat_insulations.insulation_losses import HeatLossCalculator


class MainHeatInsulations():
    def __init__(self):
        """Создаём объект с новыми данными"""
        self.heat_insulation = HeatLossCalculator()

    def update_result(self):
        self.heat_insulation = HeatLossCalculator()


main_heat_insulation = MainHeatInsulations()


