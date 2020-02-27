from rest_framework import permissions
from rest_framework.generics import CreateAPIView

from . import serializers


class PostView(CreateAPIView):

    serializer_class = serializers.PostSerializer

    def get_permissions(self):
        # decide permission based on type of request
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated,]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
