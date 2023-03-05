import openai
import pytest

from fastapi.testclient import TestClient

from src.config import settings
from src.main import app

client = TestClient(app)

openai.api_key = settings.OPENAI_API_KEY


def test_generate_images_bad_request_wrong_number_of_images():
    prompt = "test prompt"
    number_of_images = 12
    response = client.get(f"/generate-images?prompt={prompt}&number_of_images={number_of_images}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Number of images must be between 1 and 10."


def test_generate_images_bad_request_empty_prompt():
    prompt = ""
    number_of_images = 1
    response = client.get(f"/generate-images?prompt={prompt}&number_of_images={number_of_images}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Prompt can't be empty."


if __name__ == "__main__":
    pytest.main([__file__])
