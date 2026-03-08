"""Tests for feedback form rendering and feedback submission behaviour."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Feedback


class FeedbackViewTests(TestCase):
    """Test feedback page access and feedback submission flows."""

    def setUp(self):
        """Create reusable test client and an authenticated user."""
        self.client = Client()

        self.user = User.objects.create_user(
            username="student1",
            password="TestPass123",
        )

        self.valid_feedback_payload = {
            "ui": "y",
            "sug": "Improve the navigation menu.",
            "satisfy": "y",
            "sugg": "Add more advanced courses.",
            "rating": "d",
        }

    def test_feedback_page_loads(self):
        """Verify the feedback form page renders successfully."""
        response = self.client.get(reverse("feedback"))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_can_submit_feedback(self):
        """Verify feedback can be submitted without authentication."""
        response = self.client.post(
            reverse("feedback"),
            self.valid_feedback_payload,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Feedback.objects.count(), 1)

        feedback = Feedback.objects.first()
        self.assertIsNone(feedback.user)

    def test_authenticated_user_feedback_is_linked_to_user(self):
        """Verify submitted feedback is linked to the logged-in user."""
        self.client.login(username="student1", password="TestPass123")

        response = self.client.post(
            reverse("feedback"),
            self.valid_feedback_payload,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Feedback.objects.count(), 1)

        feedback = Feedback.objects.first()
        self.assertEqual(feedback.user, self.user)

    def test_invalid_feedback_submission_does_not_create_record(self):
        """Verify invalid form input does not create a feedback entry."""
        invalid_payload = {
            "ui": "",
            "sug": "",
            "satisfy": "",
            "sugg": "",
            "rating": "",
        }

        response = self.client.post(reverse("feedback"), invalid_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Feedback.objects.count(), 0)