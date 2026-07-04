from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    SERPER_API_KEY: str = ""
    OPENROUTER_API_KEY: str = ""

    OPENROUTER_DEFAULT_MODEL: str = "openai/gpt-oss-20b:free"

    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DISCORD_BOT_TOKEN: str = ""
    DISCORD_CHANNEL_ID: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()