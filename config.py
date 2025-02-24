import configparser
from pydantic import BaseModel, Field, ValidationError

class GeneralConfig(BaseModel):
    heating_hours: int = Field(default=5160, description="Количество часов отопительного периода")
    heating_summer_hours: int = Field(default=0, description="Количество часов летнего периода")

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
            heating_hours=int(config["general"]["heating_hours"]),
            heating_summer_hours=int(config["general"]["heating_summer_hours"]),
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
