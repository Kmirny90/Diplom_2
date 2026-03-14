import pytest
import requests
from generators.user_generator import generate_user_data
from data.urls import Endpoints


@pytest.fixture
def registered_user():

    user_data = generate_user_data()
    requests.post(Endpoints.REGISTER, json=user_data)
    return user_data


@pytest.fixture
def auth_token(registered_user):

    response = requests.post(
        Endpoints.LOGIN,
        json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
    )
    return response.json()["accessToken"]


@pytest.fixture
def ingredient_ids():

    response = requests.get(Endpoints.INGREDIENTS)
    data = response.json()
    ingredients = data["data"]
    return {
        "bun": next(i["_id"] for i in ingredients if i["type"] == "bun"),
        "sauce": next(i["_id"] for i in ingredients if i["type"] == "sauce"),
        "main": next(i["_id"] for i in ingredients if i["type"] == "main"),
        "invalid": "61c0c5a71d1f82001bdaaa999"
    }