import requests
import allure
from data.urls import Endpoints


class OrderMethods:

    @staticmethod
    @allure.step("Создание заказа")
    def create_order(ingredients, token=None):
        headers = {"Authorization": token} if token else {}
        data = {"ingredients": ingredients}
        return requests.post(Endpoints.ORDERS, json=data, headers=headers)