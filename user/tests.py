from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpassword',
            'password2': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '1234567890'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_register_user(self):
        url = reverse('user:register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpassword',
            'password2': 'newpassword',
            'first_name': 'New',
            'last_name': 'User',
            'phone_number': '0987654321'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_login_user(self):
        url = reverse('user:login')
        data = {
            'email': self.user.email,
            'password': 'testpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_change_password(self):
        url = reverse('user:change-password')
        data = {
            'email': self.user.email,
            'password': 'testpassword',
            'new_password': 'newpassword',
            'confirm_password': 'newpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
