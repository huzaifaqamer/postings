from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class UserLogoutViewTest(APITestCase):
    def setUp(self):
        self.base_url = reverse('user-logout')

    def login_user(self, user):
        token = Token.objects.create(user=user)
        self.client.force_authenticate(user=user, token=token)


    def test_logout_logged_in_user(self):
        user = User.objects.create_user(
            username='test',
            password='secret'
        )
        self.login_user(user)
        response = self.client.delete(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)


    def test_deny_logout_logged_out_user(self):
        user = User.objects.create_user(
            username='test',
            password='secret'
        )
        response = self.client.delete(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)