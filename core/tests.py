from django.test import TestCase
from .models import UserProfile, Role, Permission
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse_lazy


class TestUserAndProfileModel(TestCase):
    def setUp(self):
        User.objects.create_user(
            username="testuser", password="testpassword", email="test@email"
        )

    def test_profile_auto_created_for_new_user(self):
        user = User.objects.get(username="testuser")
        self.assertIsNotNone(user.profile)

    def test_creating_second_profile_raises_integrity_error(self):
        user = User.objects.get(username="testuser")
        self.assertRaises(IntegrityError, UserProfile.objects.create, user=user)

    def test_auto_user_profile_deleted(self):
        user = User.objects.get(username="testuser")
        user_id = user.id
        user.delete()
        self.assertRaises(
            UserProfile.DoesNotExist, UserProfile.objects.get, user_id=user_id
        )


class TestRoleAndPermissionModel(TestCase):
    def setUp(self):
        self.role1 = Role.objects.create(name="Test Role")
        self.role2 = Role.objects.create(name="Test Role 2")

        self.perm1 = Permission.objects.create(name="Test Permission")
        self.perm2 = Permission.objects.create(name="Test Permission 2")

        self.role1.permissions.add(self.perm1)
        self.role2.permissions.add(self.perm2)

    def test_unique_role_name(self):
        with self.assertRaises(IntegrityError):
            Role.objects.create(name="Test Role")

    def test_unique_permission_name(self):
        with self.assertRaises(IntegrityError):
            Permission.objects.create(name="Test Permission")

    def test_role_permissions(self):
        self.assertIn(self.perm1, self.role1.permissions.all())
        self.assertNotIn(self.perm2, self.role1.permissions.all())


class TestLoginAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", email="test@email"
        )

    def test_login_successful_get_token(self):
        login_path = reverse_lazy("token_obtain_pair")

        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(login_path, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_wrong_credentials_no_token(self):
        login_path = reverse_lazy("token_obtain_pair")

        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(login_path, data, format="json")

        self.assertEqual(response.status_code, 401)
        self.assertNotIn("access", response.data)
        self.assertNotIn("refresh", response.data)
