import configparser
from pydantic import BaseModel, Field, ValidationError

class GeneralConfig(BaseModel):
    heating_hours: int = Field(default=5160, description="Количество часов отопительного периода")
    heating_summer_hours: int = Field(default=0, description="Количество часов летнего периода")
    density_water: int = Field(default=1000, description="Плотность воды")
    specific_heat: int = Field(default=1, description="Удельная теплоемкость теплоносителя (ккал/(кг·°C))")
    temp_distribution_coeff: int = Field(default=0.75, description="Доля массового расхода теплоносителя, "
                                                                   "теряемого подающим трубопроводом")

class TemperatureConfig(BaseModel):
    temp_water_supplementation: int= Field(default=5, description="Температура окружающей среды (°C)")
    temp_fill_water: int = Field(default=40, description="Температура воды, используемой для заполнения трубопровода "
                                                         "(°C)")
    temp_underground: int = Field(default=5, description="Температура грунта (°C)")
    temp_aboveground: int = Field(default=-25, description="Температура воздуха (°C)")
    temp_in_channel: int = Field(default=15, description="Температура в канале (°C)")

class VolumeNetworkConfig(BaseModel):
    norm_leakage_a: float = Field(default=0.25, description="норма среднегодовой утечки теплоносителя (м³/ч×м³)")

class Config(BaseModel):
    general: GeneralConfig
    temperature: TemperatureConfig
    volume_network: VolumeNetworkConfig


def load_config(config_path: str = "constant.conf") -> Config:
    config = configparser.ConfigParser()
    config.read(config_path)

    try:
        general = GeneralConfig(
            heating_hours=int(config["general"]["heating_hours"]),
            heating_summer_hours=int(config["general"]["heating_summer_hours"]),
            density_water=int(config["general"]["density_water"]),
            specific_heat=int(config["general"]["specific_heat"]),
        )

        temperature = TemperatureConfig(
            temp_water_supplementation=int(config["temperature"]["temp_water_supplementation"]),
            temp_fill_water=int(config["temperature"]["temp_fill_water"]),
            temp_underground=int(config["temperature"]["temp_underground"]),
            temp_aboveground=int(config["temperature"]["temp_aboveground"]),
            temp_in_channel=int(config["temperature"]["temp_in_channel"]),
        )

        volume_network = VolumeNetworkConfig(
            norm_leakage_a=float(config["volume_network"]["norm_leakage_a"]),
        )

        return Config(
            general=general,
            temperature=temperature,
            volume_network=volume_network
        )

    except ValidationError as e:
        print("Ошибка в конфигурации:", e)
        raise
