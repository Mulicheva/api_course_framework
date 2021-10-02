import pytest
import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Registration cases")
class TestUserRegister(BaseCase):
    datas = [{
        'password': '123',
        'username': 'learnqa',
        'firstName': 'learnqa',
        'lastName': 'learnqa'},
        {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'},
        {
            'password': '123',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        },
        {
            'password': '123',
            'username': 'learnqa',
            'lastName': 'learnqa',
            'email': 'vinkotov@example.com'
        },
        {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'email': 'vinkotov@example.com'
        }
    ]

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Создание пользователя успешно")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.title("Создание пользователя с уже использованной почтой")
    def test_create_user_with_existing_email(self):
        email ='vinkotov@example.com'
        data =self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content{response.content}"



    @allure.title("К проверке. Создание пользователя с некорректным email - без символа @")
    def test_create_user_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"Invalid email format", f"Unexpected response content{response.content}"


    @allure.title("К проверке. Создание пользователя без указания одного из полей")
    @pytest.mark.parametrize('data', datas)
    def test_create_user_unsuccessfully(self, data):


        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)


    @allure.title("К проверке. Создание пользователя с очень коротким именем в один символ")
    def test_create_user_with_short_name(self):
        data = self.prepare_registration_data()
        data['username'] ='1'
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too short", f"Unexpected response content{response.content}"


    @allure.title("К проверке. Создание пользователя с очень длинным именем - длиннее 250 символов")
    def test_create_user_with_long_name(self):
        data = self.prepare_registration_data()
        data['username'] ='91111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too long", f"Unexpected response content{response.content}"