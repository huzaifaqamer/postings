from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def create_user():
    user = User.objects.create_user(
        username='test',
        password='test123'
    )

    return user

def login_user(client, user):
    token = Token.objects.create(user=user)
    client.force_authenticate(user=user, token=token)