from datetime import datetime

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.common import create_user, login_user
from posts.tests.common import create_post
from posts.models import Post


class PostListTest(APITestCase):
    def setUp(self):
        self.base_url = reverse('list-create-post')
        self.post_user = create_user()
        self.test_posts = [
            {'title': 'Post 1', 'body': 'Post 1 body', 'status': Post.PostStatus.DRAFT, 'author': self.post_user},
            {'title': 'Post 2', 'body': 'Post 2 body', 'status': Post.PostStatus.UNPUBLISHED, 'author': self.post_user},
            {'title': 'Post 3', 'body': 'Post 3 body', 'status': Post.PostStatus.PUBLISHED, 'author': self.post_user}
        ]
        for post in self.test_posts:
            create_post(post)

    def str_to_date(self, date_str):
        format_str = '%Y-%m-%dT%H:%M:%S.%fZ'
        return datetime.strptime(date_str, format_str)


    def test_logged_out_user_only_sees_published_posts(self):
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0].get('title'), self.test_posts[2].get('title'))


    def test_non_author_only_sees_published_posts_and_own_posts(self):
        user = create_user({'username': 'User 2', 'password': 'secret'})
        user_post = create_post({
            'title': 'User Post', 
            'body': 'User Post body', 
            'status': Post.PostStatus.DRAFT, 
            'author': user
        })
        login_user(self.client, user)
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0].get('title'), user_post.title)
        self.assertEqual(response.data[1].get('title'), self.test_posts[2].get('title'))


    def test_author_sees_all_self_posts(self):
        login_user(self.client, self.post_user)
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0].get('title'), self.test_posts[2].get('title'))
        self.assertEqual(response.data[1].get('title'), self.test_posts[1].get('title'))
        self.assertEqual(response.data[2].get('title'), self.test_posts[0].get('title'))


    def test_posts_ordered_by_descending_created_date(self):
        login_user(self.client, self.post_user)
        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.str_to_date(response.data[0].get('created_on')) > self.str_to_date(response.data[1].get('created_on')), True)
        self.assertEqual(self.str_to_date(response.data[1].get('created_on')) > self.str_to_date(response.data[2].get('created_on')), True)


    def test_post_has_only_specific_fields(self):
        valid_keys = ('id', 'title', 'status', 'created_on')
        key_checks = []
        response = self.client.get(self.base_url)

        for key in response.data[0].keys():
            key_checks.append(key in valid_keys)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(all(key_checks), True)
    