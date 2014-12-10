from hashlib import sha256
from .models import User, fixture_session


def load_data():
    user = User()
    user.email = 'test@test.com'
    user.password = sha256('12345').hexdigest()
    user.username = 'test_name'
    fixture_session.add(user)
