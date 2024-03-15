
import allure
import requests
import random
import string


class Courier:
    courier_url = "https://qa-scooter.praktikum-services.ru/api/v1/courier"
    response = None

    def generate_random_string(self, length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @allure.step("Регистрируем нового курьера.")
    def register_new_courier_and_return_login_password(self):
        login_pass = []

        login = self.generate_random_string(10)
        password = self.generate_random_string(10)
        first_name = self.generate_random_string(10)
        payload = {
            "login": login,
            "password": password,
            "firstName": first_name
        }
        self.response = requests.post(self.courier_url, data=payload)
        if self.response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)

        return login_pass

    @allure.step("Удаляем курьера.")
    def delete_courier(self, login, password):
        payload = {
            "login": login,
            "password": password
        }
        response = requests.post(self.courier_url + "/login", data=payload)
        courier_id = response.json()["id"]
        requests.delete(self.courier_url + "/:" + str(courier_id), data={"id": courier_id})
