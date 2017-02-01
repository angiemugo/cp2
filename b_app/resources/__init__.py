import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

import config


app = Flask(__name__)
api=Api(app)

app.config["DEVELOPMENT"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

from resources.models import *
from resources.auth import Login, Register
from resources.bucket import Buckets, Item

api.add_resource(Login, '/auth/login', endpoint='login')
api.add_resource(Register, '/auth/register', endpoint='register')
api.add_resource(Buckets, '/bucketlists/', endpoint='bucketlists')
api.add_resource(Buckets, '/bucketlists/<bucket_id>', endpoint='bucketlist')
api.add_resource(Item, '/bucketlists/<bucket_id>/items/', endpoint='items')
api.add_resource(Item, '/bucketlists/<bucket_id>/items/<item_id>', endpoint='item')
