from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    class PostStatus(models.TextChoices):
        DRAFT = 'D', 'Draft'
        UNPUBLISHED = 'U', 'Unpublished'
        PUBLISHED = 'P', 'Published'
    
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=1000)
    status = models.CharField(
        max_length=1,
        choices=PostStatus.choices,
        default=PostStatus.DRAFT
    )
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    @property
    def view_count(self):
        return self.postviews.views


class PostViews(models.Model):
    post = models.OneToOneField(
        Post,
        on_delete=models.CASCADE
    )
    views = models.IntegerField(default=0)