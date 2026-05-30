
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "城市感官探索家 API"
    APP_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 高德地图API配置
    AMAP_API_KEY: str = "your_amap_api_key_here"
    AMAP_BASE_URL: str = "https://restapi.amap.com/v3"

    # OpenWeatherMap API配置
    OPENWEATHER_API_KEY: str = "your_openweather_api_key_here"
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5/weather"
    OPENWEATHER_AIR_POLLUTION_URL: str = "https://api.openweathermap.org/data/2.5/air_pollution"

    # 数据库配置
    DATABASE_PATH: str = "data/sensory_marks.db"

    # 知识库路径
    KNOWLEDGE_BASE_PATH: str = "knowledge_base"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
