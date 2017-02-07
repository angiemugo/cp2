#bucketlist-check if exists, then check for lack of name, define what it should look like(reqparse)
import json
import jwt, os

from flask import abort, request, g
from flask_restful import abort, Resource, fields
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps

from cp2.resources.models import Bucket, Items
from cp2.resources.api import app, db
from cp2.resources.serializer import *


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
       if args.name is None:
           return {"message": "bucket name cannot be empty"}, 400

       search_bucketlist = Bucket.query.filter_by(name=args.name).first()
       if search_bucketlist:
           return {"message": "this bucket list already exists"}, 400

       else:
           bucketlist = Bucket(name=args.name, created_by=g.user)
           db.session.add(bucketlist)
           db.session.commit()
           return marshal(bucketlist, bucketlists_fields), 201

    @login_required
    def get(self, bucket_id=None):
        '''gets all bucketlists from database when id is none but gives one when id is chosen
        '''
        #implement query and pagination
        parser = RequestParser()
        parser.add_argument("limit", type=int, location="args")
        parser.add_argument("offset", type=int, location="args")
        parser.add_argument("q", type=str, location="args")
        args = parser.parse_args()
        limit = args.limit or 20
        offset = args.offset
        search_parameter = args.q

        if bucket_id is None:

            if search_parameter:
                named_bucketlist = Bucket.query.filter_by(created_by=g.user_id, name=search_parameter).all()
                return marshal(named_bucketlist, bucketlists_fields)

            else:
                all_bucketlists = Bucket.query.filter_by(created_by=g.user).limit(limit).offset(offset).all()
                return marshal(all_bucketlists, bucketlists_fields), 200

        else:
            parser = RequestParser()
            parser.add_argument("bucket_id", type=int, required=True)
            search_bucket = Bucket.query.filter_by(id=bucket_id, created_by=g.user).first()
            if search_bucket:
                return marshal(search_bucket, bucketlists_fields), 200
            else:
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
                return({"message": "the bucketlist you entered does not exist"}, 404)
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
            duplicate_item = Items.query.filter_by(name=args.name).first()

            if duplicate_item:
                return({"message": " this item already exists in this bucketlist"}, 409)

            else:
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
            return ("the item has been deleted")

        else:
            return ({"message": "the item you chose does not exist"}, 404)
