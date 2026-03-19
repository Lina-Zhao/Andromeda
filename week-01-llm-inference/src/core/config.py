"""
Configuration management using Pydantic settings.

Loads environment variables and provides typed configuration.
"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8080
    DEBUG: bool = False
    ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Authentication
    API_KEYS: str = "test-key-123,test-key-456"  # Comma-separated
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # vLLM Configuration
    VLLM_URL: str = "http://localhost:8000/v1"
    MODEL_NAME: str = "Qwen/Qwen2.5-7B-Instruct"
    MAX_TOKENS: int = 2048
    TEMPERATURE: float = 0.7
    
    # Monitoring
    ENABLE_METRICS: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    def get_api_keys(self) -> List[str]:
        """Parse API keys from comma-separated string."""
        return [key.strip() for key in self.API_KEYS.split(",")]


# Global settings instance
settings = Settings()
