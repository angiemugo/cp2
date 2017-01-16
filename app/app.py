from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os
from flask.ext.restful import Resource, Api, reqparse

from models import Users, Bucket, Items


app = Flask(__name__)
api = Api(app)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
db = SQLAlchemy(app)

class Users(Resource):
    def login():
        username = request.json.get(username)
        password = request.json.get(password)
        if username or password is none:
            abort(400, message = "cannot login without password or username")
        elif
        #check if password matches
    def register():
        username = request.json.get("username")
        password = request.json.get("password")
        if username is none or password is none:
            abort(400, message = "username or password cannot be blank")
        elif Users.query.filter_by(user_name = username). first() is not None:
            abort(400, message = "username already exists" )
        else:
            user = Users(user_name = username)
            user.hash_password(password)
            db.session.add(user)
            db.session.commit()
            return ("user has been successfully created", 201)



class Bucketlists(Resource):
     def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('bucket_title', type = str, required = True,
            help = 'No task title provided', location = 'json')
        super(TaskListAPI, self).__init__()


    def get_bucketlists(self):

        pass
    def create_bucketlist(self):
        pass


class Items(Resource):
     def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, location = 'json')
        self.reqparse.add_argument('description', type = str, location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        super(TaskAPI, self).__init__()

    def get_items(self,item_id):
        pass
    def create_bucketitems(self, item_id):
        pass
    def update_bucketitem(self, item_id):
        pass
    def delete_bucketitem(self, item_id):
        pass

api.add_resource(Bucketlists,'/bucketlist/buckets', endpoint="buckets")
api.add_resource(Items, "/bucketlist/buckets/<int:id>", endpoint="bucket")
api.add_resource(Users, "/auth/register")
api.add_resource(Users, "/auth/login" endpoint=user_name)




if __name__ == '__main__':
    app.run()
