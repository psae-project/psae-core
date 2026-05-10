from pydantic_settings import BaseSettings


class PSAESettings(BaseSettings):
    # Redis / Kafka
    redis_url: str = "redis://localhost:6379"
    use_kafka: bool = False

    # Stream names
    event_stream: str = "psae:events"
    signal_stream: str = "psae:signals"
    trade_stream: str = "psae:trades"

    # NLP
    finbert_model: str = "ProsusAI/finbert"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"

    # Pricing
    pricing_provider: str = "yfinance"
    polygon_api_key: str = ""

    # Risk limits
    max_single_position: float = 0.05
    max_sector_concentration: float = 0.20
    vix_kill_switch_threshold: float = 40.0
    max_gross_exposure: float = 1.5
    beta_target: float = 0.0

    class Config:
        env_file = ".env"
        env_prefix = "PSAE_"


settings = PSAESettings()
