from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./offer_rank.db"
    # Explainable ranking weights (interview talking point)
    weight_affinity: float = 0.55
    weight_recency: float = 0.25
    weight_margin: float = 0.20


settings = Settings()
