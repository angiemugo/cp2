from datetime import datetime

from passlib.apps import custom_app_context as pwd_context

from .api import db

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(500), nullable=False, unique = True )
    password = db.Column(db.String(500), nullable=False)
    buckets = db.relationship("Bucket", backref="buckets", lazy="dynamic",  cascade="all, delete-orphan")

    def hash_password(self, password):
        """hashes password
        """
        self.password_hash = pwd_context.encrypt(password)
        return self.password_hash

    def verify_password(self, password):
        """checks value given against password hash
        """
        return pwd_context.verify(password, self.password_hash)

    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)

    def __repr__(self):
        """return string representation of user object
        """
        return self.username


class Bucket(Base):
    __tablename__ = "bucket"
    items = db.relationship("Item", backref="items", lazy="dynamic",  cascade="all, delete-orphan")
    created_by = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)


class Item(Base):
    __tablename__ = "item"
    bucket_id = db.Column(db.Integer, db.ForeignKey("bucket.id"), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
