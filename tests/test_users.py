import json
from flask import jsonify
from faker import Factory
from app.test import test_setup


class TestLogin:
    def test_login_success(self):
        pass
    def test_login_fails_without_credentials(self):

        pass
    def test_login_fails_when_does_not_exist(self):
        pass
class TestRegister:
    def test_register_success(self):
        fakes = Factory.create()
        self.username = fakes.user_name()
        self.password = fakes.password()
        response = self.client.post("/auth/register",
                                 content_type="application/json",
                                 data=json.dumps({"username": self.username,
                                       "password": self.password}))
        self.assertEqual(response.status_code, 201)

    def test_register_fails_without_credentials(self):
        fakes = Factory.create()
        self.password = fakes.password()
        response = self.client.post("/auth/register",
                                    content_type="application/json",
                                    data=json.dumps({"username":self.username}))
        self.assertEqual(response.status_code, 401)

    def test_register_fails_if_user_exists(self):

        pass
