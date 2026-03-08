"""Tests for account views and account-related API endpoints."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from .models import UserProfile


class AccountViewAndApiTests(TestCase):
    """Test standard account views and role-based account API access."""

    def setUp(self):
        """Create test clients and sample teacher/student users."""
        # Client for testing standard Django views
        self.web_client = Client()

        # Client for testing DRF API endpoints
        self.api_client = APIClient()

        # Create a teacher account for permission-based tests
        self.teacher_user = User.objects.create_user(
            username="teacher1",
            password="TestPass123",
            first_name="Teach",
            last_name="Er",
        )
        self.teacher_user.userprofile.role = "teacher"
        self.teacher_user.userprofile.save()

        # Create a student account for general user tests
        self.student_user = User.objects.create_user(
            username="student1",
            password="TestPass123",
            first_name="Stu",
            last_name="Dent",
        )
        self.student_user.userprofile.role = "student"
        self.student_user.userprofile.save()

        # Create a second student account for search and list tests
        self.other_student = User.objects.create_user(
            username="student2",
            password="TestPass123",
            first_name="Second",
            last_name="Student",
        )
        self.other_student.userprofile.role = "student"
        self.other_student.userprofile.save()

    def test_register_page_loads(self):
        response = self.web_client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_register_creates_user_and_profile(self):
        response = self.web_client.post(
            reverse("register"),
            {
                "username": "newstudent",
                "email": "newstudent@example.com",
                "first_name": "New",
                "last_name": "Student",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
                "role": "student",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newstudent").exists())
        self.assertTrue(
            UserProfile.objects.filter(
                user__username="newstudent",
                role="student",
            ).exists()
        )

    def test_register_fails_with_mismatched_passwords(self):
        response = self.web_client.post(
            reverse("register"),
            {
                "username": "badstudent",
                "email": "badstudent@example.com",
                "first_name": "Bad",
                "last_name": "Student",
                "password1": "StrongPass123",
                "password2": "WrongPass123",
                "role": "student",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="badstudent").exists())

    def test_profile_requires_login(self):
        response = self.web_client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)

    def test_profile_page_loads_for_authenticated_user(self):
        self.web_client.login(username="student1", password="TestPass123")
        response = self.web_client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)

    def test_teacher_dashboard_requires_teacher_access(self):
        self.web_client.login(username="student1", password="TestPass123")
        response = self.web_client.get(reverse("teacher_dashboard"))
        self.assertNotEqual(response.status_code, 200)

    def test_teacher_dashboard_shows_students_only(self):
        self.web_client.login(username="teacher1", password="TestPass123")
        response = self.web_client.get(reverse("teacher_dashboard"))
        self.assertEqual(response.status_code, 200)
        users = response.context["users"]
        self.assertEqual(users.count(), 2)
        self.assertTrue(all(profile.role == "student" for profile in users))

    def test_teacher_dashboard_search_filters_results(self):
        self.web_client.login(username="teacher1", password="TestPass123")
        response = self.web_client.get(
            reverse("teacher_dashboard"),
            {"q": "student1"},
        )
        self.assertEqual(response.status_code, 200)
        users = response.context["users"]
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first().user.username, "student1")

    def test_teacher_dashboard_search_no_results(self):
        self.web_client.login(username="teacher1", password="TestPass123")
        response = self.web_client.get(
            reverse("teacher_dashboard"),
            {"q": "nomatch"},
        )
        self.assertEqual(response.status_code, 200)
        users = response.context["users"]
        self.assertEqual(users.count(), 0)

    def test_user_home_requires_login(self):
        response = self.web_client.get(reverse("user_home"))
        self.assertEqual(response.status_code, 302)

    def test_api_index_is_public(self):
        response = self.web_client.get(reverse("api_index"))
        self.assertEqual(response.status_code, 200)
        data = response.data
        self.assertIn("MindTopia API", data)
        self.assertIn("Public Endpoints", data["MindTopia API"])
        self.assertIn("Teacher Only Endpoints", data["MindTopia API"])

    def test_api_users_denies_unauthenticated(self):
        response = self.api_client.get(reverse("api_users"))
        self.assertEqual(response.status_code, 403)

    def test_api_users_denies_student(self):
        self.api_client.force_authenticate(user=self.student_user)
        response = self.api_client.get(reverse("api_users"))
        self.assertEqual(response.status_code, 403)

    def test_api_users_allows_teacher(self):
        self.api_client.force_authenticate(user=self.teacher_user)
        response = self.api_client.get(reverse("api_users"))
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 3)

    def test_api_students_denies_unauthenticated(self):
        response = self.api_client.get(reverse("api_students"))
        self.assertEqual(response.status_code, 403)

    def test_api_students_denies_student(self):
        self.api_client.force_authenticate(user=self.student_user)
        response = self.api_client.get(reverse("api_students"))
        self.assertEqual(response.status_code, 403)

    def test_api_students_allows_teacher_and_returns_students_only(self):
        self.api_client.force_authenticate(user=self.teacher_user)
        response = self.api_client.get(reverse("api_students"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(all(item["role"] == "student" for item in response.data))

    def test_api_user_profile_denies_unauthenticated(self):
        response = self.api_client.get(
            reverse("api_user_profile", kwargs={"username": "student1"})
        )
        self.assertEqual(response.status_code, 403)

    def test_api_user_profile_denies_student(self):
        self.api_client.force_authenticate(user=self.student_user)
        response = self.api_client.get(
            reverse("api_user_profile", kwargs={"username": "student1"})
        )
        self.assertEqual(response.status_code, 403)

    def test_api_user_profile_allows_teacher(self):
        self.api_client.force_authenticate(user=self.teacher_user)
        response = self.api_client.get(
            reverse("api_user_profile", kwargs={"username": "student1"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["user"]["username"], "student1")
        self.assertEqual(response.data["role"], "student")

    def test_api_user_profile_returns_404_for_missing_username(self):
        self.api_client.force_authenticate(user=self.teacher_user)
        response = self.api_client.get(
            reverse("api_user_profile", kwargs={"username": "missinguser"})
        )
        self.assertEqual(response.status_code, 404)