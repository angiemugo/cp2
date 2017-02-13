import json
import jwt, os

from flask import abort, request, g
from flask_restful import abort, Resource, fields
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps

from resources.models import Bucket, Item
from resources.api import app, db
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
            return{"message": "please login to access this route"}, 401
        try:
            user = get_user_id(token)

        except jwt.DecodeError:
            return {"message":"invalid token"}, 401
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
        limit = request.args.get('limit') or 20
        page = request.args.get('page') or 1
        search_parameter = request.args.get('q')
        if not bucket_id :
            '''
            if no bucket id is specified, it returns all buckets
            '''
            if search_parameter:
                '''
                if a search parameter is specified
                '''
                named_bucketlist = Bucket.query.filter_by(
                    created_by=g.user_id, name=search_parameter)\
                .paginate(int(page), int(limit))
                bucketitems = named_bucketlist.items
                if named_bucketlist is not None:
                    if named_bucketlist.has_next:
                        next_page = str(request.url_root) + \
                        'bucketlists?q=' + q + '&page=' + str(int(page) + 1) + \
                        '&&limit=' + str(int(limit))
                    else:
                        next_page = 'None'
                    if named_bucketlist.has_prev:
                        prev_page= str(request.url_root) + 'bucketlists?q=' + \
                        q + '&page=' + str(int(page) - 1)
                    else:
                        prev_page = 'None'
                    buckets = [bucket for bucket in bucketitems]
                    return {'bucketlists':marshal(buckets, bucketlists_fields),
                        'next': next_page,'prev': prev_page}
                else:
                    return {"message": "No bucketlist match was found"}, 404
            else:
                    '''
                    if no search parameter is specified
                    '''
                    all_bucketlists = Bucket.query.filter_by(
                        created_by=g.user).paginate(int(page), int(limit))
                    bucketlists = all_bucketlists.items
                    if all_bucketlists is not None:
                        if all_bucketlists.has_next:
                            next_page = str(request.url_root) + \
                            'bucketlists?' + 'page=' + str(int(page) + 1) +\
                            '&&limit=' + str(int(limit))
                        else:
                            next_page = 'None'
                        if all_bucketlists.has_prev:
                            prev_page = str(request.url_root) + \
                            'bucketlists?' + 'page=' + str(int(page) - 1) + \
                            '&&limit=' + str(int(limit))
                        else:
                            prev_page = 'None'
                        buckets = [bucket for bucket in bucketlists]
                        return {"bucketlists": marshal(buckets,
                    bucketlists_fields), 'next':next_page, 'previous':prev_page}
                    else:
                        return {"message": "no bucketlists available"}, 404
        else:
            '''
            if bucket id is specified
            '''
            search_bucket = Bucket.query.filter_by(id=bucket_id,
                                                   created_by=g.user).first()
            if search_bucket is not None:
                return marshal(search_bucket, bucketlists_fields), 200
            else:
                return {"message": "the bucketlist you chose does not exist"}, 404

    @login_required
    def put(self, bucket_id=None):
        '''
            edits a specific bucketlist according to id provided
        '''
        if bucket_id is None:
            return {"message": "no bucketlist selected"}, 401
        else:
            parser=RequestParser()
            parser.add_argument('name', type=str, required=True)
            args=parser.parse_args()
            try:
                selected_blst = Bucket.query.filter_by(id=bucket_id,
                                                       created_by=g.user).first()
                selected_blst.name = args.name
                db.session.commit()
                return marshal(selected_blst, bucketlists_fields), 201
            except NoResultFound:
                return {"message": "the bucketlist you entered does not exist"}, 404

    @login_required
    def delete(self, bucket_id=None):
        '''
        deletes a bucketlist given an id
        '''
        if bucket_id is None:
            return {"message": "no bucketlist selected"}, 401
        else:
            some_blst = Bucket.query.filter_by(id=bucket_id, created_by=g.user).one()
            if some_blst:
                db.session.delete(some_blst)
                db.session.commit()
                return {"message":"the bucketlist was deleted"}, 200
            else:
                return {"message": "the bucketlist you chose does not exist"}, 404


class Items(Resource):
    @login_required
    def post(self, bucket_id):
        '''creates items
        '''
        parser = RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("done", type=bool, required=True)
        args=parser.parse_args()
        search_bucket = Bucket.query.filter_by(id=bucket_id,
                                               created_by=g.user).first()
        if search_bucket is not None:
            # import ipdb; ipdb.set_trace()
            duplicate_item = Item.query.filter_by(name=args.name).first()
            if duplicate_item:
                return {"message": " this item already exists in this bucketlist"}, 409
            else:
                item = Item(name=args.name, bucket_id=bucket_id, done=args.done)
                db.session.add(item)
                db.session.commit()
                return marshal(item, items_fields), 201
        else:
            return {"message": "the bucketlist you chose does not exist"}, 404

    @login_required
    def put(self, bucket_id, item_id):
        '''
        edits a specific item according to id provided
        '''
        parser=RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("done", type=bool, required=True)
        args=parser.parse_args()
        selected_item = Item.query.filter_by(id=item_id).first()
        selected_item.name = args.name
        selected_item.done = args.done
        if selected_item is not None:
            db.session.commit()
            return marshal(selected_item, items_fields)
        else:
            return {"message": "the bucketlist you chose does not exist"}, 404

    @login_required
    def delete(self, bucket_id, item_id):
        '''
        deletes an item given an id
        '''
        some_item = Item.query.filter_by(id=item_id).first()
        if some_item:
            db.session.delete(some_item)
            db.session.commit()
            return "the item has been deleted"

        else:
            return {"message": "the item you chose does not exist"}, 404
