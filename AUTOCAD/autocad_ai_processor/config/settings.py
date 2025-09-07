from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # Application settings
    app_name: str = "AutoCAD 3D to 2D AI Processor"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1
    
    # File settings
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    upload_dir: str = "uploads"
    output_dir: str = "outputs"
    temp_dir: str = "temp"
    
    # AI settings
    ai_confidence_threshold: float = 0.7
    batch_size: int = 5
    max_components: int = 1000
    
    # Database settings (for future use)
    database_url: Optional[str] = None
    
    # Redis settings (for caching)
    redis_url: Optional[str] = None
    
    # Security settings
    secret_key: str = "your-secret-key-here"
    access_token_expire_minutes: int = 30
    
    # Logging settings
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    # Cleanup settings
    cleanup_interval_hours: int = 24
    max_file_age_hours: int = 72
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


# File paths
UPLOAD_DIR = os.path.join(settings.upload_dir, settings.temp_dir)
OUTPUT_DIR = os.path.join(settings.output_dir, "2d_files")
DOWNLOAD_DIR = os.path.join(settings.output_dir, "downloads")

# Create directories if they don't exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
