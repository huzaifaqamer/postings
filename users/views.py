from rest_framework import permissions
from rest_framework.generics import CreateAPIView, DestroyAPIView

from . import serializers


class UserRegisterView(CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.UserRegisterSerializer


class UserLogoutView(DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        token = self.request.user.auth_token
        return token