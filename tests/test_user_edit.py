import allure
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions

@allure.epic("Edit method cases")
class TestUserEdit(BaseCase):
    @allure.title("Редактирование только что созданного пользователя")
    def test_edit_just_created_user(self):
        #REGISTER
        register_data =self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email =register_data['email']
        first_name = register_data['firstName']
        password =register_data['password']
        user_id =self.get_json_value(response1,"id")

        #LOGIN
        login_data ={
            'email':email,
            'password':password
        }
        response2 =MyRequests.post("/user/login", data=login_data)

        auth_sid =self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        new_name ="Changed Name"

        response3 =MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token" : token},
            cookies ={"auth_sid": auth_sid},
            data ={"firstName":new_name}
        )

        Assertions.assert_code_status(response3, 200)

        #GET

        response4 =MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

    @allure.title("К проверке. Изменить данные пользователя, будучи неавторизованными")
    def test_edit_just_created_user_not_login(self):
        #REGISTER
        register_data =self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email =register_data['email']
        first_name = register_data['firstName']
        password =register_data['password']
        user_id =self.get_json_value(response1,"id")



        #EDIT
        new_name ="Changed Name"

        response3 =MyRequests.put(
            f"/user/{user_id}",
           # headers={"x-csrf-token" : token},
           # cookies ={"auth_sid": auth_sid},
            data ={"firstName":new_name}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            "utf-8") == f"Auth token not supplied", f"Unexpected response content{response3.content}"
        #GET

        response5 =MyRequests.get(
            f"/user/{user_id}"
           # headers={"x-csrf-token": token},
           # cookies={"auth_sid": auth_sid},
        )
        expected_fields = ["username"]
        unexpected_fields = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response5, expected_fields)
        Assertions.assert_json_has_not_keys(response5, unexpected_fields)


    @allure.title("К проверке. Изменить данные пользователя, авторизованными другим пользователем")
    def test_edit_another_user(self):
        #REGISTER
        register_data =self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email =register_data['email']
        first_name = register_data['firstName']
        password =register_data['password']
        user_id =self.get_json_value(response1,"id")

        #LOGIN
        login_data ={
            'email':email,
            'password':password
        }
        response2 =MyRequests.post("/user/login", data=login_data)

        auth_sid =self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        user_id_prev=str(int(user_id)-1)



        #EDIT
        new_name ="Changed Name"
        response3 =MyRequests.put(
            f"/user/{user_id_prev}",
            headers={"x-csrf-token" : token},
            cookies ={"auth_sid": auth_sid},
            data ={"username":new_name}
        )

        Assertions.assert_code_status(response3, 200)

        #GET

        response4 =MyRequests.get(
            f"/user/{user_id_prev}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )


        ##Проверим, что имя у пользователя не стало измененным
        Assertions.assert_json_value_by_name_noteq(
            response4,
            "username",
            new_name,
            "Equal name of the user after edit"
        )


    @allure.title("К проверке. Изменить данные пользователя,на новый email без символа @")
    def test_edit_same_user_bad_email(self):
        #REGISTER
        register_data =self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email =register_data['email']
        first_name = register_data['firstName']
        password =register_data['password']
        user_id =self.get_json_value(response1,"id")

        #LOGIN
        login_data ={
            'email':email,
            'password':password
        }
        response2 =MyRequests.post("/user/login", data=login_data)

        auth_sid =self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        bad_email ="Changed Name"
        response3 =MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token" : token},
            cookies ={"auth_sid": auth_sid},
            data ={"email":bad_email}
        )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            "utf-8") == f"Invalid email format", f"Unexpected response content{response3.content}"

        #GET

        response4 =MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name_noteq(
            response4,
            "email",
            bad_email,
            "Equal email of the user after edit"
        )


    @allure.title("К проверке. Изменить данные пользователя, на очень короткое значение в один символ")
    def test_edit_same_user_bad_firstName(self):
        #REGISTER
        register_data =self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)
        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email =register_data['email']
        first_name = register_data['firstName']
        password =register_data['password']
        user_id =self.get_json_value(response1,"id")

        #LOGIN
        login_data ={
            'email':email,
            'password':password
        }
        response2 =MyRequests.post("/user/login", data=login_data)

        auth_sid =self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #EDIT
        bad_firstName ="C"
        response3 =MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token" : token},
            cookies ={"auth_sid": auth_sid},
            data ={"firstName":bad_firstName}
        )

        Assertions.assert_code_status(response3, 400)
        assert "Too short value for field firstName" in response3.content.decode("utf-8")


        response4 =MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_json_value_by_name_noteq(
            response4,
            "firstName",
            bad_firstName,
            "Equal firstName of the user after edit")


