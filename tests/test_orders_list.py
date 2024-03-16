import requests
import allure


class TestOrdersList:
    @allure.title("Проверка получения списка заказов.")
    def test_orders_list_get_list_true(self):
        response = requests.get("https://qa-scooter.praktikum-services.ru/api/v1/orders/")
        assert response.status_code == 200 and response.json()["orders"] != " "

    @allure.title("Проверка получения ошибки при запросе списка заказов с несуществующим courierId.")
    def test_orders_list_get_list_with_bad_courier_id_error(self):
        response = requests.get("https://qa-scooter.praktikum-services.ru/api/v1/orders/?", params={"courierId": 0})
        assert response.status_code == 404 and response.json()["message"] == "Курьер с идентификатором 0 не найден"


