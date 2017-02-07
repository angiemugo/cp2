import json

from faker import Faker

from .test_setup import TestSetUp
from cp2.resources.models import Bucket, Items, Users
from cp2.resources.api import app, db

class TestItem(TestSetUp):
    def test_create_item_success(self):
        '''test that an item is created
        '''
        new_item = json.dumps({'name':self.fakes.word(), "done":"True", "bucket_id":1})
        response = self.app.post(
            '/bucketlists/1/items/',
            content_type="application/json",
            data=new_item,
            headers={"Authorization": self.token}
            )
        self.assertEqual(response.status_code, 201)

    def test_item_not_created_without_name(self):
        '''item is not created without name
        '''
        new_item = json.dumps({'name':None})
        response = self.app.post(
            '/bucketlists/1/items/',
            content_type="application/json",
            data=new_item,
            headers={"Authorization": self.token}
            )
        self.assertEqual(response.status_code, 400)

    def test_item_not_created_in_nonexistent_bucket(self):
        '''item is not created if bucket chosen does not exists
        '''
        new_item = json.dumps({'name':self.fakes.word()})
        response = self.app.post(
            '/bucketlists/56/items/',
            content_type="application/json",
            data=new_item,
            headers={"Authorization": self.token}
            )
        self.assertEqual(response.status_code, 400)

    def test_delete_item(self):
        new_item = json.dumps({'name':self.fakes.word()})
        response = self.app.delete(
            '/bucketlists/1/items/1',
            content_type="application/json",
            headers={"Authorization": self.token}
            )
        self.assertEqual(response.status_code, 200)

    def test_update_success(self):
        '''
        test that a bucket can be updated
        '''
        new_item = json.dumps({'name': self.fakes.word()})
        response = self.app.put(
            '/bucketlists/1/items/1',
            content_type="application/json",
            headers={"Authorization": self.token},
            data=new_item
            )
        self.assertEqual(response.status_code, 200)
