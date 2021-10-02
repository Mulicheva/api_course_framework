import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Delete method cases")
class TestUserDelete(BaseCase):
    @allure.title("К проверке. Удалить неудаляемого пользователя")
    def test_delete_undeleteble_user(self):


        #LOGIN
        data = {

            'email': 'vinkotov@example.com',

            'password': '1234'

        }

        response2 =MyRequests.post("/user/login", data=data)

        auth_sid =self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        Assertions.assert_code_status(response2, 200)
        #DELETE
        user_id = 2

        response3 =MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token" : token},
            cookies ={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            "utf-8") == f"Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f"Unexpected response content{response3.content}"

        #GET

        response4 =MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response4, 200)



    @allure.title("К проверке. Удалить пользователя свежсозданного")
    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # DELETE


        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},

        )

        Assertions.assert_code_status(response3, 200)

        # GET

        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response4, 404)

    @allure.title("К проверке. Удалить пользователя, будучи авторизованными другим пользователем")
    def test_delete_another_user(self):
        #REGISTER
        register_data =self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email =register_data['email']
        first_name = register_data['firstName']
        password =register_data['password']
        user_id =self.get_json_value(response1,"id")

        # REGISTER OTHER USER
        register_data = self.prepare_registration_data()
        responseq = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(responseq, 200)
        Assertions.assert_json_has_key(responseq, "id")

        user_idq = self.get_json_value(responseq, "id")

        #LOGIN
        login_data ={
            'email':email,
            'password':password
        }
        response2 =MyRequests.post("/user/login", data=login_data)

        auth_sid =self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")


        #DELETE

        response3 =MyRequests.delete(
            f"/user/{user_idq}",
            headers={"x-csrf-token" : token},
            cookies ={"auth_sid": auth_sid}

        )
        Assertions.assert_code_status(response3, 200)
        #GET
        #проверим что не удалили пользователя
        response4 =MyRequests.get(
            f"/user/{user_idq}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response4, 200)
