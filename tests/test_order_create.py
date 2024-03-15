import json

import allure
import pytest
import requests


class TestOrderCreate:

    @allure.title("Проверка создания заказа с выбором цветов.")
    @pytest.mark.parametrize(
        "color",
        [
            "BLACK ",
            "GREY",
            "",
            ["BLACK ", "GREY"]
        ]
    )
    def test_order_create_choose_colors_true(self, color):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": [color]
        }
        payload_string = json.dumps(payload)
        response = requests.post("https://qa-scooter.praktikum-services.ru/api/v1/orders", data=payload_string)
        assert response.status_code == 201 and response.json()["track"] != " "
