from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.common import create_user, login_user


class UserLogoutViewTest(APITestCase):
    def setUp(self):
        self.base_url = reverse('user-logout')
        

    def test_logout_logged_in_user(self):
        user = create_user()
        login_user(self.client, user)
        response = self.client.delete(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)


    def test_deny_logout_logged_out_user(self):
        user = create_user()
        response = self.client.delete(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)