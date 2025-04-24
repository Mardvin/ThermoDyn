from django.db.models import QuerySet


class ElectricityResult:
    def __init__(self, boilers_room_pump: QuerySet):
        self.__boilers_room_pump = boilers_room_pump
        # return:
        self.sum_electricity_cost = self.calculate_sum_electricity()

    def calculate_sum_electricity(self):
        total = sum(machine.power_kW * machine.operating_hours for machine in self.__boilers_room_pump)
        return total