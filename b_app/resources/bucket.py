#bucketlist-check if exists, then check for lack of name, define what it should look like(reqparse)
import json
import jwt,os

from resources.models import Bucket, Items
from resources import app, db
from flask import abort, request, g
from flask_restful import abort, Resource, fields
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from resources.serializer import *

JWT_PASS = os.environ["SECRET_KEY"]
JWT_ALGORITHM = "HS256"

def get_user_id(token):
    '''
    decode the token and get the user id.
    '''
    user = jwt.decode(token, JWT_PASS, JWT_ALGORITHM)
    g.user_id = user.get("user_id", "0")
    return user['user_id']

def login_required(func):
    '''creates a decorator to protect the routes'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return({"message":"please login to access this route"}, 401)
        try:
            user = get_user_id(token)

        except jwt.DecodeError:
            return({"message":"invalid token"}, 401)
        g.user = user
        return func(*args, **kwargs)
    return wrapper


class Buckets(Resource):
    @login_required
    def post(self):
       '''creates a bucketlists
       '''
       parser = RequestParser()
       parser.add_argument("name", type=str, required=True)
       args = parser.parse_args()
       search_bucketlist = Bucket.query.filter_by(name=args.name).first()
       if search_bucketlist:
           return {"message": "this bucket list already exists"}
       else:
           bucketlist = Bucket(name=args.name, created_by=g.user)
           db.session.add(bucketlist)
           db.session.commit()
           return marshal(bucketlist, bucketlists_fields)

    @login_required
    def get(self, bucket_id=None):
        '''gets all bucketlists from database when id is none but gives one when id is chosen
        '''
        #implement query and pagination
        if bucket_id is None:
            all_bucketlists = Bucket.query.all()
            return marshal(all_bucketlists, bucketlists_fields), 200

        else:
            parser = RequestParser()
            parser.add_argument("bucket_id", type=int, required=True)
            try:
                search_bucket = Bucket.query.filter_by(id=bucket_id, created_by=g.user).first()
                return marshal(search_bucket, bucketlists_fields)
            except NoResultFound:
                return ({"message": "the bucketlist you chose does not exist"}, 404)

    @login_required
    def put(self, bucket_id=None):
        '''
            edits a specific bucketlist according to id provided
        '''
        if bucket_id is None:
            return({"message": "no bucketlist selected"}, 401)
        else:
            parser=RequestParser()
            parser.add_argument('name', type=str, required=True)
            args=parser.parse_args()
            try:
                selected_blst = Bucket.query.filter_by(id=bucket_id, created_by=g.user).first()#add for current user
                #import ipdb; ipdb.set_trace()
                selected_blst.name = args.name
                db.session.commit()
                return marshal(selected_blst, bucketlists_fields), 201
            except NoResultFound:
                abort(404, message="the bucketlist you entered does not exist")
                #delete earlier post, right not it's creating two

    @login_required
    def delete(self, bucket_id=None):
        '''
        deletes a bucketlist given an id
        '''
        if bucket_id is None:
            return({"message": "no bucketlist selected"}, 401)
        else:
            some_blst = Bucket.query.filter_by(id=bucket_id, created_by=g.user).one()
            if some_blst:
                db.session.delete(some_blst)
                db.session.commit()
                return ({"message":"the bucketlist was deleted"}, 200)
            else:
                return ({"message": "the bucketlist you chose does not exist"}, 404)


class Item(Resource):
    @login_required
    def post(self, bucket_id):
        '''creates items
        '''
        parser = RequestParser()
        parser.add_argument("bucket_id", type=int, required=True)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("done", type=bool, required=True)

        args=parser.parse_args()
        search_bucket = Bucket.query.filter_by(id=bucket_id, created_by=g.user).first()

        if search_bucket is not None:
            item = Items(name=args.name, bucket_id=args.bucket_id, done=args.done)
            db.session.add(item)
            db.session.commit()
            return marshal(item, items_fields), 201

        else:
            return ({"message": "the bucketlist you chose does not exist"}, 404)

    @login_required
    def put(self, bucket_id, item_id):
        '''
        edits a specific item according to id provided
        '''

        parser=RequestParser()
        parser.add_argument('name', type=str, required=True)
        args=parser.parse_args()
        selected_item = Items.query.filter_by(id=item_id).first()
        selected_item.name = args.name

        if selected_item is not None:
            db.session.commit()
            return marshal(selected_item, items_fields)

        else:
            return ({"message": "the bucketlist you chose does not exist"}, 404)

    @login_required
    def delete(self, bucket_id, item_id):
        '''
        deletes an item given an id
        '''
        some_items = Items.query.filter_by(id=item_id).first()

        if some_items:
            db.session.delete(some_items)
            db.session.commit()
            return (some_items.id + "has been deleted")

        else:
            return ({"message": "the item you chose does not exist"}, 404)
