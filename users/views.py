from django.contrib.auth.models import User

from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from . import serializers

class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserRegisterSerializer

