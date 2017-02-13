import os

from unittest import TestCase
from faker import Faker

from resources.api import app, db
from resources.models import User, Bucket, Item
from resources.config import config
from resources.auth.auth import gen_auth_token


class TestSetUp(TestCase):
    def setUp(self):
        '''
        use fakes to create dummy data
        '''
        self.fakes = Faker()
        self.username = self.fakes.user_name()
        self.password = self.fakes.password()
        self.bucket_name = self.fakes.word()
        self.bucket_name1 = self.fakes.word()
        self.item_name = self.fakes.word()

        app.config.from_object(config['testing'])
        db.create_all()

        self.app = app.test_client()
        '''
        create a dummy logged in user for the protected routes
        '''
        test_user = User(username=self.username, password=self.password)
        db.session.add(test_user)
        db.session.commit()

        self.existing_user = User.query.filter_by(username=self.username).one()
        #go the login way instead shortcut
        self.token = gen_auth_token(self.existing_user)

        test_bucket = Bucket(name=self.bucket_name, created_by = self.existing_user.user_id, id=1)
        db.session.add(test_bucket)
        db.session.commit()

        test_item = Item(name=self.item_name, done= "True", bucket_id=1, id=1)
        db.session.add(test_item)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
