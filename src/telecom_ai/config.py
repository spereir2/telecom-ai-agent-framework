from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TELECOM_AI_", env_file=".env", extra="ignore")

    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "qwen2.5:7b"
    request_timeout_seconds: float = 300.0
    max_retries: int = 2


settings = Settings()
