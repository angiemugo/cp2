#bucketlist-check if exists, then check for lack of name, define what it should look like(reqparse)
import json

from resources.models import Bucket, Items
from resources import app, db
from flask import abort, request, jsonify
from flask_restful import abort, Resource, fields, marshal
from flask_restful.reqparse import RequestParser
from sqlalchemy.orm.exc import NoResultFound

items_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'bucket_id': fields.Integer,
    'done':fields.Boolean
}

bucketlists_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'items':fields.List(fields.Nested(items_fields)),
    'date_created': fields.DateTime(dt_format='rfc822'),
    'date_modified': fields.DateTime(dt_format='rfc822')
    #created_by
}


# def login_required():
#     auth = request.header.get(token)
#     if auth
#
#
#     pass

class Buckets(Resource):
    def post(self):
        '''creates a bucketlists
        '''
        parser = RequestParser()
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("created_by", type=int, required=True)
        args = parser.parse_args()
        search_bucketlist = Bucket.query.filter_by(name=args.name).first()
        if search_bucketlist:
            return {"message": "this bucket list already exists"}
        try:
            bucketlist = Bucket(name=args.name, created_by=args.created_by)
            #find out how to get created by from current user
            db.session.add(bucketlist)
            db.session.commit()

            return marshal(bucketlist, bucketlists_fields)



        except SQLALchemyError:
            db.session.rollback()
            abort(500, message='could not complete request')





    def get(self):
        '''
        gets all bucketlists from database
        '''
        all_bucketlists = Bucket.query.all()

        return marshal(all_bucketlists, bucketlists_fields)


    def put(self, bucket_id):
        '''
        edits a specific bucketlist according to id provided
        '''
        parser=RequestParser()
        parser.add_argument('name', type=str, required=True)
        args=parser.parse_args()
        try:
            selected_blst = Bucket.query.filter_by(id=bucket_id).first()#add for current user
            #import ipdb; ipdb.set_trace()
            selected_blst.name = args.name
            db.session.commit()
            return marshal(selected_blst, bucketlists_fields)
        except NoResultFound:
            abort(404, message="the bucketlist you entered does not exist")


    def delete(self, bucket_id):
        '''
        deletes a bucketlist given an id
        '''
        some_blst = Bucket.query.filter_by(id=bucket_id).one()
        if some_blst:
            db.session.delete(some_blst)
            db.session.commit()
        else:
            abort(404, message= "bucketlist you chose does not exist")


class Bucketitems(Resource):
    def get(self, bucket_id):
        '''gets all bucketlist items
        '''
        parser = RequestParser()
        parser.add_argument("bucket_id", type=int, required=True)
        try:
            search_bucket = Bucket.query.filter_by(id=bucket_id).first()
            return marshal(search_bucket, bucketlists_fields)
        except NoResultFound:
            abort(404, message="the bucketlist you chose does not exist")

class Items(Resource):
    def post(self, bucket_id):
        '''creates a bucketlists
        '''
        parser = RequestParser()
        parser.add_argument("bucket_id", type=int, required=True)
        parser.add_argument("name", type=str, required=True)
        parser.add_argument("done", type=str, required=True)
        # parser.add_argument("created_by", type=int, required=True)
        #add user to check user
        args=parser.parse_args()
        try:
            search_bucket = Bucket.query.filter_by(id=bucket_id).first()
            if search_bucket is not None:
                # import ipdb; ipdb.set_trace()
                item = Items(name=args.name, bucket_id=args.bucket_id, done=args.done)
                db.session.add(item)
                db.commit()
                return marshal(item, items_fields)
        except NoResultFound:
            abort(404, message="the bucketlist you entered does not exist")





    def put(self):
        '''
        edits a specific item according to id provided
        '''
        parser=RequestParser()
        parser.add_argument('name', type=str, required=True)
        args=parser.parse_args()
        try:
            selected_item = Items.query.filter_by(id=item_id).first()#add for current user
            #import ipdb; ipdb.set_trace()
            selected_item.name = args.name
            db.session.commit()
            return marshal(selected_item, items_fields)
        except NoResultFound:
            abort(404, message="the item you entered does not exist")



    def delete(self):
        '''
        deletes a bucketlist given an id
        '''
        some_items = Items.query.filter_by(id=item_id).one()
        if some_items:
            db.session.delete(some_items)
            db.session.commit()
        else:
            abort(404, message= "the item you chose does not exist")
