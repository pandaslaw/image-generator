import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from pydantic import BaseSettings


class AppSettings(BaseSettings):
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    OPENAI_API_KEY: str
    APP_VERSION: str = "1"
    APP_TITLE: str = "App API"
    OUTPUT_DIR = os.path.join(Path(__file__).parent.parent, "output")


load_dotenv()
settings = AppSettings()
app_configs: dict[str, Any] = {"title": settings.APP_TITLE}
