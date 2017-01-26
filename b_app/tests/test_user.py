from tests.test_setup import TestSetUp
import ipdb
import json



class TestLogin:
    def test_login_success(self):
        pass
    def test_login_fails_without_credentials(self):

        pass
    def test_login_fails_when_does_not_exist(self):
        pass
class TestRegister(TestSetUp):
    def test_register_success(self):
        self.username = self.test_user.username
        self.password = self.test_user.password
        response = self.app.post("/auth/register",
                                 content_type="application/json",
                                 data=json.dumps({"username": self.username,
                                       "password": self.password}))
        self.assertEqual(response.status_code, 201)

    def test_register_fails_without_credentials(self):
        self.username = self.test_user.username
        self.password = self.test_user.password
        response = self.app.post("/auth/register",
                                    content_type="application/json",
                                    data=json.dumps({"username":self.username}))
        self.assertEqual(response.status_code, 401)


    def test_register_fails_if_user_exists(self):
        self.username = self.test_user.username
        self.password = self.test_user.password
        response = self.app.post("/auth/register",
                                    content_type="application/json",
                                    data=json.dumps({"username":self.username}))
        response = self.app.post("/auth/register",
                                    content_type="application/json",
                                    data=json.dumps({"username":self.username}))

        self.assertEqual(response.status_code, 409)
