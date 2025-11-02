from pydantic import SecretStr
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

from .logger import logger


env_path = Path(__file__).parent.parent.parent

class Settings(BaseSettings):
    """
    Pydantic settings class to load environment variables from a .env file.
    """
    
    # Model config to load from .env file
    # It automatically finds the .env file in the current directory.
    model_config = SettingsConfigDict(
        env_file=env_path, 
        env_file_encoding='utf-8',
        extra='ignore'
    )

    OPENAI_API_KEY: SecretStr | None = None
    GEMINI_API_KEY: SecretStr
    TAVILY_API_KEY: SecretStr
    
    # Per agent LLM Configuration
    VALIDATOR_MODEL_PROVIDER: str = "google"
    VALIDATOR_MODEL_id: str = "gemini-2.0-flash"

    RESEARCHER_MODEL_PROVIDER: str = "google"
    RESEARCHER_MODEL_ID: str = "gemini-2.0-flash"
    
    COPYWRITER_MODEL_PROVIDER: str = "google"
    COPYWRITER_MODEL_ID: str = "gemini-2.0-flash"
    
    EDITOR_MODEL_PROVIDER: str = "google"
    EDITOR_MODEL_ID: str = "gemini-2.0-flash"

    # MinIO Configuration
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: SecretStr
    MINIO_BUCKET_NAME: str

    VALIDATION_THRESHOLD: int = 50  # Minimum viability score to pass validation
try:
    settings = Settings()
except Exception as e:
    logger.error(f"Error loading settings: {e}")
    logger.error("Please ensure your .env file is correctly set up in 'services/agent_content_crew'.")
    exit(1)