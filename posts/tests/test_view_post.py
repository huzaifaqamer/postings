from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.common import create_user, login_user
from posts.tests.common import create_post_with_views
from posts.models import Post, PostViews


class PostListTest(APITestCase):
    def setUp(self):
        self.post_user = create_user()
        data_test_posts = [
            {'title': 'Post 1', 'body': 'Post 1 body', 'status': Post.PostStatus.DRAFT, 'author': self.post_user},
            {'title': 'Post 2', 'body': 'Post 2 body', 'status': Post.PostStatus.UNPUBLISHED, 'author': self.post_user},
            {'title': 'Post 3', 'body': 'Post 3 body', 'status': Post.PostStatus.PUBLISHED, 'author': self.post_user}
        ]
        self.test_posts = []
        for post in data_test_posts:
            self.test_posts.append(create_post_with_views(post))

        self.draft_url = reverse('retrieve-update-post', args=[self.test_posts[0].pk])
        self.unpublished_url = reverse('retrieve-update-post', args=[self.test_posts[1].pk])
        self.published_url = reverse('retrieve-update-post', args=[self.test_posts[2].pk])


    def test_logged_out_user_can_only_view_published_posts(self):
        # DRAFT POST
        response = self.client.get(self.draft_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # UNPUBLISHED POST
        response = self.client.get(self.unpublished_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # PUBLISHED POST
        response = self.client.get(self.published_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), self.test_posts[2].title)


    def test_non_author_can_only_view_published_posts_of_others(self):
        user = create_user({'username': 'User 2', 'password': 'secret'})
        login_user(self.client, user)

        # DRAFT POST
        response = self.client.get(self.draft_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # UNPUBLISHED POST
        response = self.client.get(self.unpublished_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # PUBLISHED POST
        response = self.client.get(self.published_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), self.test_posts[2].title)


    def test_author_can_view_all_self_posts(self):
        login_user(self.client, self.post_user)

        # DRAFT POST
        response = self.client.get(self.draft_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), self.test_posts[0].title)

        # UNPUBLISHED POST
        response = self.client.get(self.unpublished_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), self.test_posts[1].title)
        
        # PUBLISHED POST
        response = self.client.get(self.published_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('title'), self.test_posts[2].title)


    def test_post_views_increase_when_logged_out_user_views_it(self):
        initial_view_count = PostViews.objects.get(post_id=self.test_posts[2].pk).views
        response = self.client.get(self.published_url)
        final_view_count = PostViews.objects.get(post_id=self.test_posts[2].pk).views

        self.assertEqual(response.data.get('views'), final_view_count)
        self.assertEqual(final_view_count, initial_view_count + 1)


    def test_post_views_increase_when_non_author_views_it(self):
        user = create_user({'username': 'User 2', 'password': 'secret'})
        login_user(self.client, user)

        initial_view_count = PostViews.objects.get(post_id=self.test_posts[2].pk).views
        response = self.client.get(self.published_url)
        final_view_count = PostViews.objects.get(post_id=self.test_posts[2].pk).views

        self.assertEqual(response.data.get('views'), final_view_count)
        self.assertEqual(final_view_count, initial_view_count + 1)


    def test_post_views_not_increase_when_author_views_it(self):
        login_user(self.client, self.post_user)

        initial_view_count = PostViews.objects.get(post_id=self.test_posts[2].pk).views
        response = self.client.get(self.published_url)
        final_view_count = PostViews.objects.get(post_id=self.test_posts[2].pk).views

        self.assertEqual(response.data.get('views'), initial_view_count)
        self.assertEqual(final_view_count, initial_view_count)