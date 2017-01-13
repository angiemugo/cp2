from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.restful import Resource, Api



app = Flask(__name__)
api = Api(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
db = SQLAlchemy(app)

class Users(Resource):
    def login():
        pass
    def register():
        pass


class Bucketlists(Resource):

    def get_bucketlists(self):
        pass
    def add_bucketlist(self):
        pass
    def update_bucketlist(self):
        pass
    def delete_bucketlist(self):
        pass


class Items(Resource):
    def get_items(self,item_id):
        pass
    def add_bucketitems(self, item_id):
        pass
    def update_bucketitem(self, item_id):
        pass
    def delete_bucketitem(self, item_id):
        pass






if __name__ == '__main__':
    app.run()
