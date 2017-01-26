from resources import db
from passlib.apps import custom_app_context as pwd_context



class Users(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(500), nullable=False, unique = True )
    password = db.Column(db.String(500), nullable=False)
    buckets = db.relationship("Bucket", backref="buckets", lazy="dynamic",  cascade="all, delete-orphan")



    def hash_password(self, password):
        '''hashes password
        '''
        self.password_hash = pwd_context.encrypt(password)
        return self.password_hash



    def verify_password(self, password):
        '''checks value given against password hash
        '''
        return pwd_context.verify(password, self.password_hash)



    def __init__(self, username, password):
        self.username = username
        self.password = self.hash_password(password)






class Bucket(db.Model):
    __tablename__ = "bucket"
    bucket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bucket_name = db.Column(db.String(200), nullable=False, unique=True)
    bucket_items = db.relationship("Items", backref="items", lazy="dynamic",  cascade="all, delete-orphan")
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

class Items(db.Model):
    __tablename__ = "items"
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(200), nullable=False, unique=True)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    bucket_id = db.Column(db.Integer, db.ForeignKey("bucket.bucket_id"), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
