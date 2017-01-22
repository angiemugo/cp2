import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from b_app.config import config

app = Flask(__name__)

loaded_config = os.environ.get('APP_SETTINGS')
app.config.from_object(config[loaded_config])

db = SQLAlchemy(app)

# To avoid cyclic imports
from b_app.models import *
