from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ModelForge API"
    app_version: str = "0.1.0"
    environment: str = "development"
    database_url: str
    max_upload_size_mb: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()