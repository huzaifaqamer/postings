from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.common import create_user


class UserLoginViewTest(APITestCase):
    def setUp(self):
        self.base_url = reverse('user-login')


    def test_login_user_with_correct_credentials(self):
        user = create_user()
        data = {
            'username': user.username,
            'password': 'test123'
        }
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], user.auth_token.key)


    def test_not_login_user_with_invalid_credentials(self):
        user = create_user()
        data = {
            'username': 'test',
            'password': 'invalid'
        }
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_not_login_user_if_empty_request(self):
        data = {}
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)