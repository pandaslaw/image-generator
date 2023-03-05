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

# import pytest
# from async_asgi_testclient import TestClient
# from fastapi import status
#
# from src.auth.constants import ErrorCode
#
#
# @pytest.mark.asyncio
# async def test_register(client: TestClient) -> None:
#     resp = await client.post(
#         "/auth/users",
#         json={
#             "email": "email@fake.com",
#             "password": "123Aa!",
#         },
#     )
#     resp_json = resp.json()
#
#     assert resp.status_code == status.HTTP_201_CREATED
#     assert resp_json == {"email": "email@fake.com"}
#
#
# @pytest.mark.asyncio
# async def test_register_email_taken(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
#     from src.auth.dependencies import service
#
#     async def fake_getter(*args, **kwargs):
#         return True
#
#     monkeypatch.setattr(service, "get_user_by_email", fake_getter)
#
#     resp = await client.post(
#         "/auth/users",
#         json={
#             "email": "email@fake.com",
#             "password": "123Aa!",
#         },
#     )
#     resp_json = resp.json()
#
#     assert resp.status_code == status.HTTP_400_BAD_REQUEST
#     assert resp_json["detail"] == ErrorCode.EMAIL_TAKEN