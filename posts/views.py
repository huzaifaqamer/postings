from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from posts.models import Post
from . import serializers
from posts.permissions import IsAuthorOrReadOnly
from posts.filters import IsViewablePostFilterBackend


class PostView(ListCreateAPIView):

    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    filter_backends = (IsViewablePostFilterBackend, OrderingFilter)
    ordering = ['-created_on']

    def get_permissions(self):
        # decide permission based on type of request
        if self.request.method == 'GET':
            self.permission_classes = (permissions.AllowAny,)
        elif self.request.method == 'POST':
            self.permission_classes = (permissions.IsAuthenticated,)

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostRetrieveUpdateView(RetrieveUpdateAPIView):

    queryset = Post.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (IsViewablePostFilterBackend,)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PostDetailSerializer
        elif self.request.method in ('PUT', 'PATCH'):
            return serializers.PostSerializer

    # increment view count
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user != instance.author:
            instance.postviews.views += 1
            instance.postviews.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)