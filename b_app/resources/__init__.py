import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config


app = Flask(__name__)

app.config["DEVELOPMENT"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DATABASE_URL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# loaded_config = os.environ.get('APP_SETTINGS')
# print (loaded_config)
#app.config.from_object(config[loaded_config])

db = SQLAlchemy(app)

#To avoid cyclic imports
from resources.models import *
