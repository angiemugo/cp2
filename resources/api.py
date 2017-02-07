import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

from .config import config


app = Flask(__name__)
api = Api(app)

# load config from environment variable
config_name = os.environ.get('APP_SETTINGS', 'default')
app.config.from_object(config[config_name])

db = SQLAlchemy(app)

from .models import Users, Bucket, Items
from .auth.auth import Login, Register
from .bucket.bucket import Buckets, Item

api.add_resource(Login, '/auth/login', endpoint='login')
api.add_resource(Register, '/auth/register', endpoint='register')
api.add_resource(Buckets, '/bucketlists/', endpoint='bucketlists')
api.add_resource(Buckets, '/bucketlists/<bucket_id>', endpoint='bucketlist')
api.add_resource(Item, '/bucketlists/<bucket_id>/items/', endpoint='items')
api.add_resource(Item, '/bucketlists/<bucket_id>/items/<item_id>', endpoint='item')
