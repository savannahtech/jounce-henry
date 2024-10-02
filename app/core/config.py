import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "LLM Benchmark Simulation"
    PROJECT_DESCRIPTION: str = "Benchmarking various LLMs against quality metrics."
    PROJECT_VERSION: str = "1.0.0"

    DATABASE_URL: str
    REDIS_URL: str
    SECRET_KEY: str
    LLM_NAMES: list[str] = [
        "GPT-4o",
        "Llama 3.1 405",
        "Mistral Large2",
        "Claude 3.5 Sonnet",
        "Gemini 1.5 Pro",
        "GPT-4o mini",
        "Llama 3.1 70B",
        "amba 1.5Large",
        "Mixtral 8x22B",
        "Gemini 1.5Flash",
        "Claude 3 Haiku",
        "Llama 3.1 8B",
    ]
    METRICS_NAMES: list[str] = ["TTFT", "TPS", "e2e_latency", "RPS"]

    class Config:
        env_file = ".env"


settings = Settings()
