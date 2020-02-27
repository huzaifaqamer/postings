from posts.models import Post
from users.tests.common import create_user

def create_post(data=None):
    if data is None:
        user = create_user()
        data = {
            'title': 'Test Post',
            'body': 'Test body',
            'status': Post.PostStatus.Draft,
            'author': user
        }
    
    post = Post.objects.create(**data)
    return post