import allure
import pytest
import requests
from data.urls import Endpoints
from data.user_data import ERROR_MESSAGES


@allure.suite("Логин пользователя")
class TestLoginUser:

    @allure.title("Успешный логин пользователя")
    def test_login_existing_user_success(self, created_user):
        response = requests.post(
            Endpoints.LOGIN,
            json={
                "email": created_user["email"],
                "password": created_user["password"]
            }
        )

        assert response.status_code == 200

    @allure.title("Логин с неверным логином")
    def test_login_wrong_login_fails(self, created_user):
        response = requests.post(
            Endpoints.LOGIN,
            json={
                "email": "wrong_login_12345@test.ru",
                "password": created_user["password"]
            }
        )

        assert response.status_code == 401
        assert response.json()["message"] == ERROR_MESSAGES["incorrect_login"]

    @allure.title("Логин с неверным паролем")
    def test_login_wrong_password_fails(self, created_user):
        response = requests.post(
            Endpoints.LOGIN,
            json={
                "email": created_user["email"],
                "password": "wrong_password_12345"
            }
        )

        assert response.status_code == 401
        assert response.json()["message"] == ERROR_MESSAGES["incorrect_login"]

    @pytest.mark.parametrize("missing_field", ["email", "password"])
    @allure.title("Логин без поля {missing_field}")
    def test_login_without_required_field_fails(self, created_user, missing_field):
        payload = {
            "email": created_user["email"],
            "password": created_user["password"]
        }
        payload[missing_field] = ""

        response = requests.post(Endpoints.LOGIN, json=payload)

        assert response.status_code == 401
        assert response.json()["message"] == ERROR_MESSAGES["incorrect_login"]