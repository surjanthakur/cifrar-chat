from pydantic_settings import BaseSettings, SettingsConfigDict

from pathlib import Path

env_file_path = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    """
    with this class we can access env variable in any file in folder
    """

    redis_username: str
    redis_password: str
    redis_port: int = 6379
    redis_host: str

    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
