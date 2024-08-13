from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from uuid import uuid4
from blog.models import Post

User = get_user_model()

class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
            first_name="Test",
            last_name="User",
            phone_number="1234567890"
        )
        self.client.login(email="testuser@example.com", password="password123")
        self.post_url = reverse('post-list')
        self.single_post_url = lambda post_id: reverse('post-detail', args=[post_id])
    
    def test_create_post(self):
        data = {
            "title": "New Post",
            "content": "This is a new post."
        }
        response = self.client.post(self.post_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get().title, "New Post")

    def test_read_post(self):
        post = Post.objects.create(
            title="Read Post",
            content="This post is for reading.",
            author=self.user
        )
        response = self.client.get(self.single_post_url(post.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Read Post")
        self.assertEqual(response.data['content'], "This post is for reading.")

    def test_update_post(self):
        post = Post.objects.create(
            title="Update Post",
            content="This post will be updated.",
            author=self.user
        )
        data = {
            "title": "Updated Post",
            "content": "This post has been updated."
        }
        response = self.client.put(self.single_post_url(post.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get().title, "Updated Post")
        self.assertEqual(Post.objects.get().content, "This post has been updated.")

    def test_delete_post(self):
        post = Post.objects.create(
            title="Delete Post",
            content="This post will be deleted.",
            author=self.user
        )
        response = self.client.delete(self.single_post_url(post.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

    def test_list_posts(self):
        Post.objects.create(title="Post 1", content="Content 1", author=self.user)
        Post.objects.create(title="Post 2", content="Content 2", author=self.user)
        response = self.client.get(self.post_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['title'], "Post 1")
        self.assertEqual(response.data['results'][1]['title'], "Post 2")
