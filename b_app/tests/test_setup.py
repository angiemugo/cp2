import os

from unittest import TestCase
from faker import Faker

from resources.api import app, db
# from resources.models import Users, Bucket, Items
from resources.config import config

class TestSetUp(TestCase):
    # def create_app(self):
    #     import ipdb; ipdb.set_trace()
    #
    #     return app

    def setUp(self):
        fakes = Faker()
        self.username = fakes.user_name()
        # self.username1 = fakes.user_name()
        self.password = fakes.password()
        # self.password1 = fakes.password()
        self.bucket_name = fakes.word()
        self.item_name = fakes.word()

        app.config.from_object(config.config['testing'])
        db.create_all()

        self.app = app.test_client()

        # self.test_user = Users(username=self.username, password=self.password)
        # db.session.add(self.test_user)
        # db.session.commit()

        # self.test_user1 = Users(username=self.username1, password=self.password1)
        # db.session.add(self.test_user1)
        # db.session.commit()

        # self.test_bucket = Bucket(bucket_name = self.bucket_name)
        # db.session.add(self.test_bucket)
        # db.session.commit()
        #
        # self.test_item = Items(item_name = self.item_name)
        # db.session.add(self.test_item)
        # db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
