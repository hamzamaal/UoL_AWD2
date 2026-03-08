"""Basic smoke tests for the core app."""

from django.test import TestCase


class ExampleTestCase(TestCase):
    """Confirm that the test suite is configured correctly."""

    def test_example(self):
        """Verify that the testing framework can execute a simple assertion."""
        self.assertEqual(1 + 1, 2)
