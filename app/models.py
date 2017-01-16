from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


class Users(db.Model):
    __tablename__ = 'user_data'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(200),nullable=False, unique = True )
    password = db.Column(db.String(50), nullable=False)
    buckets = db.relationship("Bucket", backref="buckets", lazy="dynamic",  cascade="all, delete-orphan"))

class Bucket(db.Model):
     __tablename__ = "bucket_data"
     bucket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     bucket_name = db.Column(db.String(200), nullable=False, unique=True)
     bucket_items = db.relationship("Items", backref="items", lazy="dynamic",  cascade="all, delete-orphan"))
     date_created = db.Column(db.DateTime, default=DateTime.utcnow)
     date_modified = db.Column(db.DateTime, default=DateTime.utcnow)
     created_by = db.Column(db.Integer, db.ForeignKey("user_id"), nullable=False)


class Items(db.Model):
     __tablename__ = "items_data"
     item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     item_name = db.Column(db.String(200), nullable=False, unique=True)
     date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
     date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
     bucket_id = db.Column(db.Integer, db.ForeignKey("bucket_id"), nullable=False)
     status = db.Column(db.Boolean, nullable=False)

def create_db(db_name):
    db = db_name + '.db'
    engine = create_engine('sqlite:///' + db)
    Base.metadata.create_all(engine)

    return engine



create_db('somedb')
