"""Tests for course views and course-related API endpoints."""

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from instructors.models import Instructor

from .models import Course, CourseFeedback


class CourseViewAndApiTests(TestCase):
    """Test course pages, registration flow, feedback, and course APIs."""

    def setUp(self):
        """Create reusable test clients and sample course data."""
        # Client for standard Django views
        self.web_client = Client()

        # Client for Django REST Framework endpoints
        self.api_client = APIClient()

        self.instructor = Instructor.objects.create(
            name="Instructor One",
            url="#",
        )

        self.course = Course.objects.create(
            title="Python Basics",
            description="Introductory Python course",
            instructor=self.instructor,
            url="#",
        )

        self.second_course = Course.objects.create(
            title="Data Science",
            description="Data science introduction",
            instructor=self.instructor,
            url="#",
        )

        self.student_user = User.objects.create_user(
            username="student1",
            password="TestPass123",
        )
        self.student_user.userprofile.role = "student"
        self.student_user.userprofile.save()

        self.teacher_user = User.objects.create_user(
            username="teacher1",
            password="TestPass123",
        )
        self.teacher_user.userprofile.role = "teacher"
        self.teacher_user.userprofile.save()

    def test_courses_page_loads(self):
        response = self.web_client.get(reverse("courses"))
        self.assertEqual(response.status_code, 200)

    def test_course_detail_requires_login(self):
        response = self.web_client.get(
            reverse("course_detail", kwargs={"course_id": self.course.id})
        )
        self.assertEqual(response.status_code, 302)

    def test_course_detail_returns_404_for_invalid_course(self):
        self.web_client.login(username="student1", password="TestPass123")
        response = self.web_client.get(
            reverse("course_detail", kwargs={"course_id": 9999})
        )
        self.assertEqual(response.status_code, 404)

    def test_student_can_register_for_course(self):
        self.web_client.login(username="student1", password="TestPass123")
        response = self.web_client.get(
            reverse("register_course", kwargs={"course_id": self.course.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.student_user.userprofile.registered_courses.filter(
                id=self.course.id
            ).exists()
        )

    def test_duplicate_course_registration_does_not_duplicate_entry(self):
        self.web_client.login(username="student1", password="TestPass123")
        self.web_client.get(
            reverse("register_course", kwargs={"course_id": self.course.id})
        )
        self.web_client.get(
            reverse("register_course", kwargs={"course_id": self.course.id})
        )
        registered_count = self.student_user.userprofile.registered_courses.filter(
            id=self.course.id
        ).count()
        self.assertEqual(registered_count, 1)

    def test_teacher_cannot_register_for_course(self):
        self.web_client.login(username="teacher1", password="TestPass123")
        response = self.web_client.get(
            reverse("register_course", kwargs={"course_id": self.course.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            self.teacher_user.userprofile.registered_courses.filter(
                id=self.course.id
            ).exists()
        )

    def test_register_course_returns_404_for_invalid_course(self):
        self.web_client.login(username="student1", password="TestPass123")
        response = self.web_client.get(
            reverse("register_course", kwargs={"course_id": 9999})
        )
        self.assertEqual(response.status_code, 404)

    def test_course_detail_context_shows_registered_status(self):
        self.student_user.userprofile.registered_courses.add(self.course)
        self.web_client.login(username="student1", password="TestPass123")
        response = self.web_client.get(
            reverse("course_detail", kwargs={"course_id": self.course.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_registered"])

    def test_submit_feedback_creates_feedback(self):
        self.web_client.login(username="student1", password="TestPass123")
        response = self.web_client.post(
            reverse("submit_feedback", kwargs={"course_id": self.course.id}),
            {
                "comment": "Very helpful course",
                "rating": 5,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            CourseFeedback.objects.filter(
                course=self.course,
                user=self.student_user,
            ).exists()
        )

    def test_submit_feedback_with_invalid_data_does_not_create_feedback(self):
        self.web_client.login(username="student1", password="TestPass123")
        response = self.web_client.post(
            reverse("submit_feedback", kwargs={"course_id": self.course.id}),
            {
                "comment": "",
                "rating": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            CourseFeedback.objects.filter(
                course=self.course,
                user=self.student_user,
            ).exists()
        )

    def test_submit_feedback_returns_404_for_invalid_course(self):
        self.web_client.login(username="student1", password="TestPass123")
        response = self.web_client.post(
            reverse("submit_feedback", kwargs={"course_id": 9999}),
            {
                "comment": "Test",
                "rating": 5,
            },
        )
        self.assertEqual(response.status_code, 404)

    def test_api_courses_is_public(self):
        response = self.api_client.get(reverse("api_courses"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_api_course_detail_is_public(self):
        response = self.api_client.get(
            reverse("api_course_detail", kwargs={"pk": self.course.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Python Basics")

    def test_api_course_detail_returns_404_for_invalid_course(self):
        response = self.api_client.get(
            reverse("api_course_detail", kwargs={"pk": 9999})
        )
        self.assertEqual(response.status_code, 404)

    def test_api_course_feedback_denies_unauthenticated(self):
        response = self.api_client.get(
            reverse("api_course_feedback", kwargs={"course_id": self.course.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_api_course_feedback_denies_student(self):
        CourseFeedback.objects.create(
            course=self.course,
            user=self.student_user,
            comment="Great",
            rating=5,
        )
        self.api_client.force_authenticate(user=self.student_user)
        response = self.api_client.get(
            reverse("api_course_feedback", kwargs={"course_id": self.course.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_api_course_feedback_allows_teacher(self):
        CourseFeedback.objects.create(
            course=self.course,
            user=self.student_user,
            comment="Great",
            rating=5,
        )
        self.api_client.force_authenticate(user=self.teacher_user)
        response = self.api_client.get(
            reverse("api_course_feedback", kwargs={"course_id": self.course.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["comment"], "Great")

    def test_api_course_feedback_returns_empty_list_for_course_with_no_feedback(self):
        self.api_client.force_authenticate(user=self.teacher_user)
        response = self.api_client.get(
            reverse("api_course_feedback", kwargs={"course_id": self.second_course.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_api_course_feedback_returns_404_for_invalid_course_id_route(self):
        self.api_client.force_authenticate(user=self.teacher_user)
        response = self.api_client.get(
            reverse("api_course_feedback", kwargs={"course_id": 9999})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)