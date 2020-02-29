from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.common import create_user, login_user
from posts.models import Post, PostViews


class PostCreateTest(APITestCase):
    def setUp(self):
        self.base_url = reverse('list-create-post')

    
    def test_create_post_if_user_logged_in(self):
        data = {
            'title': 'Test Post',
            'body': 'A test post.',
            'status': 'D'
        }
        user = create_user()
        login_user(self.client, user)
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, data['title'])
        self.assertEqual(Post.objects.get().author_id, user.pk)


    def test_not_create_post_if_user_logged_out(self):
        data = {
            'title': 'Test Post',
            'body': 'A test post.',
            'status': 'D'
        }
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_not_create_post_if_title_missing(self):
        data = {
            'body': 'A test post.',
            'status': 'D'
        }
        user = create_user()
        login_user(self.client, user)
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_not_create_post_if_body_missing(self):
        data = {
            'title': 'Test Post',
            'status': 'D'
        }
        user = create_user()
        login_user(self.client, user)
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_post_if_status_missing(self):
        data = {
            'title': 'Test Post',
            'body': 'A test post.'
        }
        user = create_user()
        login_user(self.client, user)
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().status, Post.PostStatus.DRAFT)


    def test_not_create_post_if_invalid_status(self):
        data = {
            'title': 'Test Post',
            'body': 'A test post.',
            'status': 'A'
        }
        user = create_user()
        login_user(self.client, user)
        response = self.client.post(self.base_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_new_post_creates_related_post_view(self):
        data = {
            'title': 'Test Post',
            'body': 'A test post.',
            'status': 'D'
        }
        user = create_user()
        login_user(self.client, user)
        response = self.client.post(self.base_url, data)

        post = Post.objects.get()
        post_views = PostViews.objects.get()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(PostViews.objects.count(), 1)
        self.assertTrue(hasattr(post, 'postviews'))
        self.assertEqual(post.postviews.pk, post_views.pk)
        self.assertEqual(post_views.views, 0)