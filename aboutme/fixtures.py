from hashlib import sha256
from .models import User, test_session


TEST_PASSWORD = '12345'
TEST_USERNAME = 'test_name'


def load_data():
    user = User()
    user.email = 'test@test.com'
    user.password = sha256(TEST_PASSWORD).hexdigest()
    user.username = TEST_USERNAME
    test_session.add(user)
