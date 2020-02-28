from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.tests.common import create_user, login_user
from posts.tests.common import create_post
from posts.models import Post


class PostUpdateTest(APITestCase):
    
    def test_author_can_update_complete_post(self):
        post = create_post()
        login_user(self.client, post.author)

        new_data = {
            'title': 'Published Post',
            'body': 'Published Post Body',
            'status': Post.PostStatus.PUBLISHED
        }
        url = reverse('retrieve-update-post', args=[post.pk])
        response = self.client.put(url, new_data)

        updated_post = Post.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_post.id, post.id)
        self.assertEqual(updated_post.title, new_data['title'])
        self.assertEqual(updated_post.body, new_data['body'])
        self.assertEqual(updated_post.status, new_data['status'])
        self.assertNotEqual(updated_post.title, post.title)
        self.assertNotEqual(updated_post.body, post.body)
        self.assertNotEqual(updated_post.status, post.status)


    def test_author_can_update_individual_fields(self):
        post = create_post()
        login_user(self.client, post.author)

        new_data = {
            'status': Post.PostStatus.PUBLISHED
        }
        url = reverse('retrieve-update-post', args=[post.pk])
        response = self.client.patch(url, new_data)

        updated_post = Post.objects.get()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_post.id, post.id)
        self.assertEqual(updated_post.status, new_data['status'])
        self.assertEqual(updated_post.title, post.title)
        self.assertEqual(updated_post.body, post.body)
        self.assertNotEqual(updated_post.status, post.status)


    def test_non_author_cannot_update_post(self):
        author = create_user()
        published_post = create_post({
            'title': 'Test Post',
            'body': 'Test body',
            'status': Post.PostStatus.PUBLISHED,
            'author': author
        })
        user_data = {
            'username': 'testuser2',
            'password': 'secret'
        }
        non_author = create_user(user_data)
        login_user(self.client, non_author)
        new_data = {
            'title': 'DRAFT Post',
            'body': 'DRAFT Post Body',
            'status': Post.PostStatus.DRAFT
        }
        
        url = reverse('retrieve-update-post', args=[published_post.pk])
        response = self.client.put(url, new_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)