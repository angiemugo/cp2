from datetime import datetime

from passlib.apps import custom_app_context as pwd_context

from .api import db
# model name should be singular

class Users(db.Model):
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








class Bucket(db.Model):
    __tablename__ = "bucket"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    items = db.relationship("Items", backref="items", lazy="dynamic",  cascade="all, delete-orphan")
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
    created_by = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)



class Items(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    bucket_id = db.Column(db.Integer, db.ForeignKey("bucket.id"), nullable=False)
    done = db.Column(db.Boolean, nullable=False)
