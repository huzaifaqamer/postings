from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.common import create_user


class UserRegisterViewTest(APITestCase):
    def setUp(self):
        self.base_url = reverse('user-register')

    
    def test_register_user_with_minimum_fields(self):
        data = {
            'username': 'test',
            'password': 'secret',
            'retype_password': 'secret'
        }
        response = self.client.post(self.base_url, data)

        expected_response = {
            'username': 'test',
            'first_name': '',
            'last_name': '',
            'email': ''
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data, expected_response)


    def test_register_user_with_all_fields(self):
        data = {
            'username': 'test',
            'password': 'secret',
            'retype_password': 'secret',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@examplle.com'
        }
        response = self.client.post(self.base_url, data)

        expected_response = {
            'username': 'test',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@examplle.com'
        }
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.data, expected_response)


    def test_not_register_user_without_username(self):
        data = {
            'password': 'secret',
            'retype_password': 'secret'
        }
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_not_register_user_without_password(self):
        data = {
            'username': 'test',
            'retype_password': 'secret'
        }
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_not_register_user_without_retype_password(self):
        data = {
            'username': 'test',
            'password': 'secret'
        }
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_not_register_user_with_invalid_email(self):
        data = {
            'username': 'test',
            'password': 'secret',
            'retype_password': 'secret',
            'email': 'invalid_email'
        }
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_not_register_user_with_mismatch_password(self):
        data = {
            'username': 'test',
            'password': 'secret',
            'retype_password': 'new_secret'
        }
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_not_register_user_if_username_exist(self):
        user = create_user()
        data = {
            'username': user.username,
            'password': 'secret',
            'retype_password': 'secret'
        }
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)