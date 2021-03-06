import json

from django.test import TestCase, Client

# Create your tests here.
from accounts.models import User, Profile


class LoginTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        user = User.objects.create_user(
            username='17000000001',
            password='123',
            nickname='t1'
        )
        Profile.objects.create(user=user, username=user.username)

    def test_user_login_passed(self):
        response = self.client.post('accounts/user/api/login/', {
            'username': '17000000001',
            'password': '123',
        })
        self.assertEqual(response.status_code, 200)

    def test_user_login_failure(self):
        response = self.client.post('accounts/user/api/login/', {
            'username': '17000000001',
            'password': '1234',
        })
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('密码不正确', str(data))
