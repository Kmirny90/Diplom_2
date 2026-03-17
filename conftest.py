import pytest
import requests
from generators.user_generator import generate_user_data
from data.urls import Endpoints


@pytest.fixture
def random_user():

    return generate_user_data()


@pytest.fixture
def created_user(random_user):

    response = requests.post(Endpoints.REGISTER, json=random_user)
    user_data = response.json()

    user_info = {
        **random_user,
        "accessToken": user_data.get("accessToken")
    }

    yield user_info


    if user_info.get("accessToken"):
        headers = {"Authorization": user_info["accessToken"]}
        requests.patch(Endpoints.USER, headers=headers)


@pytest.fixture
def auth_token(created_user):

    response = requests.post(
        Endpoints.LOGIN,
        json={
            "email": created_user["email"],
            "password": created_user["password"]
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


@pytest.fixture
def user_cleanup():

    users_to_delete = []
    yield users_to_delete

    for user in users_to_delete:
        login_response = requests.post(
            Endpoints.LOGIN,
            json={"email": user["email"], "password": user["password"]}
        )
        if login_response.status_code == 200:
            token = login_response.json()["accessToken"]
            requests.patch(Endpoints.USER, headers={"Authorization": token})