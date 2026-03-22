from django.test import TestCase

from .models import User


class UserModelTests(TestCase):
    def test_public_handle_is_generated(self):
        user = User.objects.create_user(username="artist", password="testpass1234")

        self.assertTrue(user.public_handle.startswith("creator-"))
