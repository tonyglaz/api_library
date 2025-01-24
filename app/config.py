# Способ управления конфигурацией приложения с использованием Pydantic для валидации и загрузки настроек из окружения
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5433
    DB_NAME: str = "api_library"
    DB_USER: str = "admin"
    DB_PASSWORD: str = "1234qwer"
    SECRET_KEY: str = "somesecret"
    ALGORITHM: str = "HS256"
    # Передает путь к e.env-файлу
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(
            os.path.abspath(__file__)), "..", ".env")
    )


settings = Settings()


def get_db_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")
