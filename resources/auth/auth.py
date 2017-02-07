import jwt
import os, json

from flask import abort, request, g
from flask_restful import abort, Resource
from flask_restful.reqparse import RequestParser
from passlib.apps import custom_app_context as pwd_context

from cp2.resources.api import app, db
from cp2.resources.models import Users

JWT_PASS = os.environ["SECRET_KEY"]
JWT_ALGORITHM = "HS256"


def verify_user(username, password):
    """
    checks for password given against password_hash to verify user
    """
    user = Users.query.filter_by(username=username).first()

    if user and pwd_context.verify(password, user.password):
        g.user_id = user.user_id

        return user



def gen_auth_token(user):
    """
    generates token once user is verified
    """
    data = {"user_id": user.user_id}

    token = jwt.encode(data, JWT_PASS, JWT_ALGORITHM)
    return token.decode('utf-8')


class Register(Resource):
    def post(self):
        """
        takes in username and password to register user
        """
        parser=RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args=parser.parse_args()
        username=args.username
        password=args.password

        if username is None or password is None:
            abort(400, message="username or password cannot be blank")
        else:
            user = Users.query.filter_by(username=username).first()
            print(user)
            if user:
                abort(400, message= "user already exists, choose another name")
            else:
                user = Users(username=username, password=password)
                db.session.add(user)
                db.session.commit()

                return("user successfully added", 201)

class Login(Resource):
    def post(self):
        """
        takes in password and username to login existing user
        """
        parser = RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()
        username = args.username
        password = args.password

        user = verify_user(username, password)
        if user:
            token = gen_auth_token(user)
            return({"token": token},200)
        else:
            abort(401, message="Wrong username or password.")
