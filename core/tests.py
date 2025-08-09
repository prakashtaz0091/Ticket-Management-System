from django.test import TestCase
from .models import UserProfile, Role, Permission
from django.contrib.auth.models import User
from django.db.utils import IntegrityError


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
        role1 = Role.objects.create(name="Test Role")
        role2 = Role.objects.create(name="Test Role 2")

        perm1 = Permission.objects.create(name="Test Permission")
        perm2 = Permission.objects.create(name="Test Permission 2")

        role1.permissions.add(perm1)
        role2.permissions.add(perm2)

    def test_unique_role_name(self):
        self.assertRaises(IntegrityError, Role.objects.create, name="Test Role")

    def test_unique_permission_name(self):
        self.assertRaises(
            IntegrityError, Permission.objects.create, name="Test Permission"
        )

    def test_role_permissions(self):
        role1 = Role.objects.get(name="Test Role")
        perm1 = Permission.objects.get(name="Test Permission")

        perm2 = Permission.objects.get(name="Test Permission 2")
        self.assertIn(perm1, role1.permissions.all())
        self.assertNotIn(perm2, role1.permissions.all())
