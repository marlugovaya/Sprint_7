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
        response = requests.post(courier.courier_url+"/login", data=payload)
        assert response.status_code == 200 and response.json()["id"] != " "
        courier.delete_courier(login, password)

    @allure.title("Проверка попытки авторизации курьера с неверным заполнением поля.")
    @pytest.mark.parametrize(
        "bad_field",
        [
            "login",
            "password"
        ]
    )
    def test_courier_login_wrong_field_false(self, bad_field):
        courier = Courier()
        login_pass = courier.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        if bad_field == "login":
            login = "this_is_a_bad_field"
        else:
            password = "this_is_a_bad_field"

        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(courier.courier_url + "/login", data=payload)
        assert response.status_code == 404 and response.json()["message"] == "Учетная запись не найдена"

    @allure.title("Проверка попытки авторизации курьера без заполнения обязательного поля.")
    @pytest.mark.parametrize(
        "bad_field",
        [
            "login",
            "password"
        ]
    )
    def test_courier_login_without_field_false(self, bad_field):
        courier = Courier()
        login_pass = courier.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        if bad_field == "login":
            login = ""
        else:
            password = ""

        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(courier.courier_url + "/login", data=payload)
        assert response.status_code == 400 and response.json()["message"] == "Недостаточно данных для входа"



