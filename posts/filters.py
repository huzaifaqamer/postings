from django.db.models import Q

from rest_framework import filters

from posts.models import Post


class IsViewablePostFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(
            Q(status=Post.PostStatus.PUBLISHED) |
            Q(author_id=request.user.id)
        )