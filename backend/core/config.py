from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    ai_provider: str = "ollama"
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "qwen2.5:7b"
    embed_model: str = "mxbai-embed-large"
    chroma_path: str = "./chroma_data"
    db_url: str = "postgresql://palo:palo@localhost:5444/palo_rag"


settings = Settings()
