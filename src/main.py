import datetime as dt
import os
from typing import List, Dict

import openai
import requests
from PIL import Image
from fastapi import FastAPI, HTTPException, status
from loguru import logger

from src.config import app_configs, settings
from src.image_size import ImageSize

app = FastAPI(**app_configs)
openai.api_key = settings.OPENAI_API_KEY


@app.get("/generate-images")
async def generate_images(prompt: str, number_of_images: int = 1, image_size: ImageSize = ImageSize.BIG,
                          save_to_disk: bool = True) -> Dict[str, List[str]]:
    """
    Creates n original images (1-10 images at a time) given a text prompt. Generated images can have a size
    of 256x256, 512x512, or 1024x1024 pixels. Smaller sizes are faster to generate.
    """

    logger.debug(f"Generating {number_of_images} image(s) of {image_size.value} size using the following prompt: "
                 f"'{prompt}'. Save to disk: {save_to_disk}.")

    try:
        number_of_images = int(number_of_images)
    except ValueError:
        number_of_images = -1

    if number_of_images < 1 or number_of_images > 10:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Number of images must be between 1 and 10.")
    if not prompt:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Prompt can't be empty.")

    response = openai.Image.create(prompt=prompt, n=number_of_images, size=image_size.value)

    if not response or not response["data"]:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate images.")

    if save_to_disk and settings.OUTPUT_DIR:
        base_path = settings.OUTPUT_DIR
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        for item in response.data:
            img = Image.open(requests.get(item.url, stream=True).raw)
            file_name = f"img_{dt.datetime.now().strftime('%Y%m%dT%H%M%S')}.png"
            img.save(os.path.join(base_path, file_name))

    return {"images": [item["url"] for item in response["data"]]}
