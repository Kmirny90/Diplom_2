import allure
import pytest
import requests
from generators.user_generator import generate_user_data
from data.urls import Endpoints
from data.user_data import ERROR_MESSAGES



class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_cleanup):
        user_data = generate_user_data()
        response = requests.post(Endpoints.REGISTER, json=user_data)

        assert response.status_code == 200
        user_cleanup.append(user_data)

    @allure.title("Создание уже существующего пользователя")
    def test_create_existing_user(self, created_user):
        response = requests.post(Endpoints.REGISTER, json=created_user)

        assert response.status_code == 403
        assert response.json()["message"] == ERROR_MESSAGES["user_exists"]

    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    @allure.title("Создание пользователя без поля {missing_field}")
    def test_create_user_without_required_field(self, missing_field):
        user_data = generate_user_data()
        del user_data[missing_field]

        response = requests.post(Endpoints.REGISTER, json=user_data)

        assert response.status_code == 403
        assert response.json()["message"] == ERROR_MESSAGES["required_fields"]
