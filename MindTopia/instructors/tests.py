"""Tests for the instructors page and instructor listing behaviour."""

from django.test import Client, TestCase
from django.urls import reverse

from .models import Instructor


class InstructorViewTests(TestCase):
    """Test instructor page rendering with and without instructor records."""

    def setUp(self):
        """Create a reusable test client."""
        self.client = Client()

    def test_instructors_page_loads(self):
        """Verify the instructors page renders successfully."""
        response = self.client.get(reverse("instructors"))
        self.assertEqual(response.status_code, 200)

    def test_instructors_page_displays_instructor_names(self):
        """Verify saved instructors appear on the rendered page."""
        Instructor.objects.create(
            name="Instructor One",
            url="#",
        )
        Instructor.objects.create(
            name="Instructor Two",
            url="#",
        )

        response = self.client.get(reverse("instructors"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Instructor One")
        self.assertContains(response, "Instructor Two")

    def test_instructors_page_handles_empty_list(self):
        """Verify the page still renders when no instructors exist."""
        response = self.client.get(reverse("instructors"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No instructors available")