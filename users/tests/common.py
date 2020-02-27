from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


def create_user(data=None):
    if data is None:
        data = {
            'username': 'test',
            'password': 'test123'
        }
    
    user = User.objects.create_user(**data)

    return user

def login_user(client, user):
    token = Token.objects.create(user=user)
    client.force_authenticate(user=user, token=token)