from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="THESISTWIN_")

    database_url: str = "sqlite:///./thesistwin.db"
    cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()
