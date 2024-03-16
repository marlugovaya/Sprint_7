import allure
import pytest
import requests

from courier import Courier


class TestCourierCreate:
    @allure.title("Проверка создания курьера со всеми обязательными полями.")
    def test_courier_create_all_required_fields_ok_true(self):
        courier = Courier()
        login_pass = courier.register_new_courier_and_return_login_password()
        assert courier.response.status_code == 201 and courier.response.json()["ok"] == True
        courier.delete_courier(login_pass[0], login_pass[1])

    @allure.title("Проверка попытки создания курьеров с одинаковыми логинами.")
    def test_courier_create_two_equal_logins_error(self):
        courier = Courier()
        login_pass = courier.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = login_pass[1]
        first_name = login_pass[2]
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(courier.courier_url, data=payload)
        assert response.status_code == 409 and response.json()[
            "message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.title("Проверка попытки создания курьера без обязательного поля.")
    @pytest.mark.parametrize(
        "f_field, s_field",
        [
            ("password", "firstName"),
            ("login", "firstName")
        ]
    )
    def test_courier_create_without_field_error(self, f_field, s_field):
        courier = Courier()
        f_field_text = courier.generate_random_string(10)
        s_field_text = courier.generate_random_string(10)
        payload = {
            f_field: f_field_text,
            s_field: s_field_text
        }
        response = requests.post(courier.courier_url, data=payload)
        assert response.status_code == 400 and response.json()[
            "message"] == "Недостаточно данных для создания учетной записи"

    @allure.title("Проверка попытки создания курьера с уже существующим логином.")
    def test_courier_create_existed_login_error(self):
        courier = Courier()
        login_pass = courier.register_new_courier_and_return_login_password()
        login = login_pass[0]
        password = courier.generate_random_string(10)
        first_name = courier.generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        response = requests.post(courier.courier_url, data=payload)
        assert response.status_code == 409 and response.json()[
            "message"] == "Этот логин уже используется. Попробуйте другой."
