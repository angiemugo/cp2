from factory import faker
from app.app import Users, Bucket, Items

class Setup(Testcase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["TEST_DB_URL"]
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setup(self):
        fakes = Faker()
        self.username = self.fakes.user_name()
        self.password = self.fakes.password()
        self.bucket_name = self.bucket_name()
        self.item_name = self.item_name()
        test_app = self.create_app()
        self.app = test_app.test_client()

        test_user = User(username = self.user_name, password = self.password)
        db.session.add(test_user)
        db.session.commit()

        test_bucket = Bucket(bucket_name = self.bucket_name)
        db.session.add(test_bucket)
        db.session.commit()

        test_item = Items(item_name = self.item_name)
        db.session.add(test_item)
        db.session.commit()
    def teardown(self):
        db.session.remove()
        db.drop_all
