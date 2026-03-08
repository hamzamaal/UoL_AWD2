"""Tests for donation page access control and authenticated rendering."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class DonateViewTests(TestCase):
    """Test donate page authentication requirements and page rendering."""

    def setUp(self):
        """Create reusable test client and an authenticated user."""
        self.client = Client()

        self.user = User.objects.create_user(
            username="donor1",
            password="TestPass123",
        )

    def test_donate_page_requires_login(self):
        """Verify anonymous users are redirected to login."""
        response = self.client.get(reverse("donate"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_access_donate_page(self):
        """Verify a logged-in user can view the donate page."""
        self.client.login(username="donor1", password="TestPass123")
        response = self.client.get(reverse("donate"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Donation")