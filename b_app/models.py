from b_app import db

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False, unique = True )
    password = db.Column(db.String(50), nullable=False)
    buckets = db.relationship("Bucket", backref="buckets", lazy="dynamic",  cascade="all, delete-orphan")

class Bucket(db.Model):
     bucket_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     bucket_name = db.Column(db.String(200), nullable=False, unique=True)
     bucket_items = db.relationship("Items", backref="items", lazy="dynamic",  cascade="all, delete-orphan")
     date_created = db.Column(db.DateTime, server_default=db.func.now())
     date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
     created_by = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)

class Items(db.Model):
     item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
     item_name = db.Column(db.String(200), nullable=False, unique=True)
     date_created = db.Column(db.DateTime, server_default=db.func.now())
     date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
     bucket_id = db.Column(db.Integer, db.ForeignKey("bucket.bucket_id"), nullable=False)
     status = db.Column(db.Boolean, nullable=False)
