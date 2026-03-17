import requests
import allure
from data.urls import Endpoints


class UserMethods:

    @staticmethod
    @allure.step("Создание пользователя")
    def create_user(user_data):
        return requests.post(Endpoints.REGISTER, json=user_data)

    @staticmethod
    @allure.step("Авторизация пользователя")
    def login_user(email, password):
        data = {"email": email, "password": password}
        return requests.post(Endpoints.LOGIN, json=data)

    @staticmethod
    @allure.step("Удаление пользователя")
    def delete_user(access_token):
        headers = {"Authorization": access_token}
        return requests.patch(Endpoints.USER, headers=headers)