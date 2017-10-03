from flask_restful import marshal, fields

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
    'date_modified': fields.DateTime(dt_format='rfc822'),
    'created_by': fields.Integer
}
