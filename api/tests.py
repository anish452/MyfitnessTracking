from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class UserAuthTestCase(APITestCase):

    def setUp(self):
        self.register_url = reverse('register')          # /api/auth/register/
        self.token_url = reverse('token')   # /api/token/

    # ----------------- Registration -----------------
    def test_user_registration_success(self):
        data = {
            "username": "alice",
            "email": "alice@example.com",
            "password": "Test1234!"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="alice").exists())

    def test_user_registration_missing_fields(self):
        data = {"username": "", "password": ""}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicate_username(self):
        User.objects.create_user(username="alice", password="Test1234!")
        data = {"username": "alice", "password": "AnotherPass123"}
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ----------------- Login -----------------
    def test_login_success(self):
        User.objects.create_user(username="bob", password="Test1234!")
        data = {"username": "bob", "password": "Test1234!"}
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password(self):
        User.objects.create_user(username="bob", password="Test1234!")
        data = {"username": "bob", "password": "WrongPass!"}
        response = self.client.post(self.token_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
