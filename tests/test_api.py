import unittest
import json

class TestBucket:
    def test_creates_bucket(self):
        test_bucketlist = json.dumps({"bucket_title": "thisbucket"})
        #headers, insert auth here
        self.client.post(#headers
                        body = test_bucketlist,
                        content_type = "application/json"
                        )



    def test_create_fails_without_name(self):
        pass
    def test_create_fails_without_authentication(self):
        pass
    def test_create_fails_with_existing_name(self):
        pass
    def test_get_fails_without_authentication(self):
        pass

class TestBucketItem:
    def test_creates_item(self):
        pass
    def test_create_item_fails_without_name(self):
        pass
    def test_create_item_fails_without_description(self):
        pass
    def test_create_item_fails_without_authentication(self):
        pass
    def test_get_bucket(self):
        pass
    def test_update_bucket(self):
        pass
    def test_delete_bucket(self):
        pass
