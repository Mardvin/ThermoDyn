import configparser
from pydantic import BaseModel, Field, ValidationError

class GeneralConfig(BaseModel):
    mass_per_year: float = Field(gt=0, description="Масса утилизируемого теплоносителя за год (кг)")
    density: float = Field(gt=0, description="Плотность теплоносителя (кг/м³)")
    specific_heat: float = Field(gt=0, description="Удельная теплоёмкость (Дж/(кг·°C))")
    temp_distribution_coeff: float = Field(ge=0, le=1, description="Коэффициент распределения (0-1)")
    heat_utilization_coeff: float = Field(ge=0, le=1, description="Коэффициент использования тепла (0-1)")

class TemperatureConfig(BaseModel):
    temp_stage1: float = Field(description="Температура первой стадии (°C)")
    temp_stage2: float = Field(description="Температура второй стадии (°C)")
    ambient_temp: float = Field(description="Температура окружающей среды (°C)")

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
            mass_per_year=float(config["general"]["mass_per_year"]),
            density=float(config["general"]["density"]),
            specific_heat=float(config["general"]["specific_heat"]),
            temp_distribution_coeff=float(config["general"]["temp_distribution_coeff"]),
            heat_utilization_coeff=float(config["general"]["heat_utilization_coeff"]),
        )

        temperature = TemperatureConfig(
            temp_stage1=float(config["temperature"]["temp_stage1"]),
            temp_stage2=float(config["temperature"]["temp_stage2"]),
            ambient_temp=float(config["temperature"]["ambient_temp"]),
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
