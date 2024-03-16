import allure
import pytest
import requests

from courier import Courier


class TestCourierLogin:
    @allure.title("Проверка авторизации курьера со всеми обязательными полями.")
    def test_courier_login_all_required_fields_true(self):
        courier = Courier()
        login_pass = courier.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(courier.courier_url + "/login", data=payload)
        assert response.status_code == 200 and response.json()["id"] != " "
        courier.delete_courier(login, password)

    @allure.title("Проверка попытки авторизации курьера с неверным заполнением поля.")
    def test_courier_login_wrong_field_false(self):
        courier = Courier()
        login_pass = courier.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        payloads = [
            {"login": login,
             "password": "this_is_bad_field"},
            {"login": "this_is_bad_field",
             "password": password},
        ]
        for p in payloads:
            response = requests.post(courier.courier_url + "/login", data=p)
            assert response.status_code == 404 and response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Проверка попытки авторизации курьера без заполнения обязательного поля.")
    def test_courier_login_without_field_false(self):
        courier = Courier()
        login_pass = courier.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        payloads = [
            {"login": login,
             "password": ""},
            {"login": "",
             "password": password},
        ]
        for p in payloads:
            response = requests.post(courier.courier_url + "/login", data=p)
            assert response.status_code == 400 and response.json()["message"] == "Недостаточно данных для входа"
