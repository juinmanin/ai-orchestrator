from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "AI Quota Orchestrator"
    app_version: str = "1.0.0"
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    
    # Security
    jwt_secret: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    encryption_key: str = "your-encryption-key-change-in-production"
    
    # Telegram
    telegram_bot_token: str = ""
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "https://open-crow.com"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
