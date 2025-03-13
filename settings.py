from pydantic_settings import BaseSettings
from pydantic import Field

from dotenv import load_dotenv

load_dotenv(override=True)

class Settings(BaseSettings):
    ASSEMBLYAI_API_KEY: str = Field(..., env="ASSEMBLYAI_API_KEY")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
