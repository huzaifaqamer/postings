from posts.models import Post, PostViews
from users.tests.common import create_user

def create_post(data=None):
    if data is None:
        user = create_user()
        data = {
            'title': 'Test Post',
            'body': 'Test body',
            'status': Post.PostStatus.DRAFT,
            'author': user
        }
    
    post = Post.objects.create(**data)
    return post


def create_post_with_views(data=None):
    post = create_post(data)
    PostViews.objects.create(post=post)
    return post