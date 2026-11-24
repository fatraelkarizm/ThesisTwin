from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="THESISTWIN_")

    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
