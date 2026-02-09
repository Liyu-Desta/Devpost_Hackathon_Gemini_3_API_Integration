"""Application configuration and settings."""
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Configuration
    API_V1_PREFIX: str = Field(..., description="API version prefix")
    PROJECT_NAME: str = Field(..., description="Project name")
    VERSION: str = Field(..., description="Application version")
    
    # Gemini API Configuration - must be provided via environment variables
    GEMINI_API_KEY: str = Field(..., description="Gemini API key from Google")
    GEMINI_MODEL: str = Field(..., description="Gemini model name to use")
    
    # CORS Configuration - can be comma-separated string or list
    CORS_ORIGINS: str = Field(..., description="Comma-separated list of allowed CORS origins")
    
    # Application Settings
    DEBUG: bool = Field(..., description="Enable debug mode")
    MAX_UPLOAD_SIZE: int = Field(..., description="Maximum upload size in bytes")
    
    def get_cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        if isinstance(self.CORS_ORIGINS, str):
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return self.CORS_ORIGINS
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
