from django.db.models import Q
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from posts.models import Post
from . import serializers
from posts.permissions import IsAuthorOrReadOnly


class PostView(ListCreateAPIView):

    serializer_class = serializers.PostSerializer

    def get_permissions(self):
        # decide permission based on type of request
        if self.request.method == 'GET':
            self.permission_classes = (permissions.AllowAny,)
        elif self.request.method == 'POST':
            self.permission_classes = (permissions.IsAuthenticated,)

        return super().get_permissions()

    def get_queryset(self):
        posts = Post.objects.filter(
            Q(status=Post.PostStatus.PUBLISHED) |
            Q(author_id=self.request.user.id)
        )
        return posts.order_by('-created_on')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateView(RetrieveUpdateAPIView):

    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        posts = Post.objects.filter(
            Q(status=Post.PostStatus.PUBLISHED) |
            Q(author_id=self.request.user.id)
        )
        return posts

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return serializers.PostSerializer