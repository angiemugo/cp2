import json

from faker import Faker

from .test_setup import TestSetUp
from cp2.resources.api import app, db
from cp2.resources.models import Bucket, Item, User


class TestBucket(TestSetUp):

    def test_create_bucket_success(self):
        '''test that a bucket is created
        '''
        new_bucket = json.dumps({'name':self.fakes.word()})
        response = self.app.post(
            '/bucketlists/',
            content_type="application/json",
            data=new_bucket,
            headers={"Authorization": self.token}
            )
        self.assertEqual(response.status_code, 201)

    def test_create_fails_without_name(self):
        '''test that if name is null post fails
        '''
        new_bucket = json.dumps({'name': None})
        response = self.app.post(
            '/bucketlists/',
            content_type="application/json",
            data=new_bucket,
            headers={"Authorization": self.token}
            )
        self.assertEqual(response.status_code, 400)

    def test_create_fails_with_same_name(self):
        '''
        when a bucket_name already esists, same cannot be created
        '''
        new_bucket = json.dumps({'name':self.bucket_name})
        response = self.app.post(
            '/bucketlists/',
            content_type="application/json",
            data=new_bucket,
            headers={"Authorization": self.token}
            )
        self.assertEqual(response.status_code, 400)


    def test_cannot_read_nonexistent_id(self):
        '''
        if a non existent id is specified, an error is raised
        '''
        new_bucket = json.dumps({'name': self.fakes.word()})

        response = self.app.get(
            '/bucketlists/234',
            content_type="application/json",
            headers={"Authorization": self.token},
            data=new_bucket
            )
        self.assertEqual(response.status_code, 404)

    def test_get_success(self):
        '''
        test that a get is successful
        '''
        response = self.app.get(
            '/bucketlists/1',
            content_type="application/json",
            headers={"Authorization": self.token}
            )
        self.assertEqual(response.status_code, 200)

    # def test_pagination(self):
    #     '''
    #     test that limit works and pagination
    #     '''
    #     response = self.app.get(
    #         '/bucketlists?page=1',
    #         content_type="application/json",
    #         headers={"Authorization": self.token}
    #         )
    #     self.assertEqual(response.status_code, 200)
    #
    #     response = self.app.get(
    #         '/bucketlists?page=2',
    #         content_type="application/json",
    #         headers={"Authorization": self.token}
    #         )
    #     self.assertEqual(response.status_code, 200)

    def test_delete_success(self):
        '''
        test that delete works
        '''
        response = self.app.delete(
        '/bucketlists/1',
        content_type="application/json",
        headers={"Authorization": self.token}
        )
        self.assertEqual(response.status_code, 200)

    def test_cannot_access_protected_routes_without_authentication(self):
        '''
        test that without authentication, cannot access protected routes
        '''
        another_bucket = json.dumps({"name": self.bucket_name, "created_by":self.existing_user.user_id})

        response = self.app.delete(
            '/bucketlists/1',
            content_type="application/json",
            data=another_bucket)
        self.assertEqual(response.status_code,401)
