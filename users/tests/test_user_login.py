from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase


class UserLoginViewTest(APITestCase):
    def setUp(self):
        self.base_url = reverse('user-login')


    def test_login_user_with_correct_credentials(self):
        user = User.objects.create_user(
            username='test',
            password='test123'
        )
        data = {
            'username': 'test',
            'password': 'test123'
        }
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], user.auth_token.key)


    def test_not_login_user_with_invalid_credentials(self):
        user = User.objects.create_user(
            username='test',
            password='test123'
        )
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