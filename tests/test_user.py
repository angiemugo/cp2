from .test_setup import TestSetUp
from cp2.resources.models import Users
from cp2.resources.api import app, db
import json

class TestRegister(TestSetUp):
    def test_register_success(self):
        response = self.app.post(
            '/auth/register',
            content_type="application/json",
            data=json.dumps({"username": self.fakes.user_name(), "password": self.fakes.password()})
            )
        self.assertEqual(response.status_code, 201)

    def test_register_fails_without_credentials(self):
        response = self.app.post(
            '/auth/register',
            content_type="application/json",
            data=json.dumps({"username":self.username})
            )
        self.assertEqual(response.status_code, 400)


    def test_register_fails_if_user_exists(self):
        response = self.app.post(
            '/auth/register',
            content_type="application/json",
            data=json.dumps({"username":self.username, "password":self.password})
            )
        self.assertEqual(response.status_code, 400)

class TestLogin(TestSetUp):
    def test_login_success(self):
        response = self.app.post(
            '/auth/login',
            content_type="application/json",
            data=json.dumps({"username":self.username, "password":self.password})
            )
        self.assertEqual(response.status_code, 200)

    def test_login_fails_without_credentials(self):
        response = self.app.post(
            '/auth/login',
            content_type="application/json",
            data=json.dumps({"username":self.username})
            )
        self.assertEqual(response.status_code, 400)#wrong error code


    def test_login_fails_when_does_not_exist(self):
        response = self.app.post(
            '/auth/login',
            content_type="application/json",
            data=json.dumps({"username":"angela", "password":"nzdsiibfjsh"})
            )
        self.assertEqual(response.status_code, 401)

    def test_token_created(self):
        response = self.app.post(
            '/auth/login',
            content_type = "application/json",
            data=json.dumps({"username":self.username, "password":self.password})
            )
        self.assertEqual(response.status_code, 200), self.token
