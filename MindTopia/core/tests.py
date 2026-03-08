"""Basic smoke tests for the core application."""

from django.test import TestCase


class ExampleTestCase(TestCase):
    """Simple test to confirm the test suite runs correctly."""

    def test_example(self):
        """Verify that the testing framework executes assertions."""
        self.assertEqual(1 + 1, 2)