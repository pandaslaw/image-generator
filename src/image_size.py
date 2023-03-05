from enum import Enum


class ImageSize(Enum):
    """Definition of image sizes supported by OpenAI Images API."""

    SMALL = "256x256"
    MEDIUM = "512x512"
    BIG = "1024x1024"
