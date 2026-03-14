import allure
import requests
from data.urls import Endpoints


@allure.suite("Заказы")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth_success(self, auth_token, ingredient_ids):
        ingredients = [ingredient_ids["bun"], ingredient_ids["sauce"]]

        response = requests.post(
            Endpoints.ORDERS,
            json={"ingredients": ingredients},
            headers={"Authorization": auth_token}
        )

        assert response.status_code == 200
        body = response.json()
        assert "order" in body
        assert body["order"]["number"] > 0

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth_success(self, ingredient_ids):
        ingredients = [ingredient_ids["bun"], ingredient_ids["main"]]

        response = requests.post(
            Endpoints.ORDERS,
            json={"ingredients": ingredients}
        )

        assert response.status_code == 200
        body = response.json()
        assert "order" in body
        assert body["order"]["number"] > 0

    @allure.title("Создание заказа с ингредиентами (без проверки авторизации)")
    def test_create_order_with_ingredients_success(self, ingredient_ids):
        ingredients = [ingredient_ids["bun"], ingredient_ids["sauce"], ingredient_ids["main"]]

        response = requests.post(
            Endpoints.ORDERS,
            json={"ingredients": ingredients}
        )

        assert response.status_code == 200
        body = response.json()
        assert "order" in body
        assert body["order"]["number"] > 0

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_fails(self, auth_token):
        response = requests.post(
            Endpoints.ORDERS,
            json={"ingredients": []},
            headers={"Authorization": auth_token}
        )

        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_hash_fails(self, auth_token, ingredient_ids):
        ingredients = [ingredient_ids["bun"], ingredient_ids["invalid"]]

        response = requests.post(
            Endpoints.ORDERS,
            json={"ingredients": ingredients},
            headers={"Authorization": auth_token}
        )

        assert response.status_code == 500