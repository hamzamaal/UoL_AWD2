"""Tests for quiz page routing and course-linked quiz behaviour."""

from django.test import Client, TestCase
from django.urls import reverse

from courses.models import Course
from instructors.models import Instructor

from .models import Quiz


class QuizViewTests(TestCase):
    """Test quiz home routing, course quiz rendering, and empty states."""

    def setUp(self):
        """Create reusable client, instructor, courses, and quiz questions."""
        self.client = Client()

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
            description="Data science course",
            instructor=self.instructor,
            url="#",
        )

        self.empty_course = Course.objects.create(
            title="Empty Course",
            description="Course without quiz questions",
            instructor=self.instructor,
            url="#",
        )

        self.quiz_one = Quiz.objects.create(
            course=self.course,
            question="What is Python?",
            option1="Snake",
            option2="Programming Language",
            option3="Car",
            option4="Game",
            answer="b",
        )

        self.quiz_two = Quiz.objects.create(
            course=self.second_course,
            question="What is data science?",
            option1="Art",
            option2="Cooking",
            option3="Field of study",
            option4="Sport",
            answer="c",
        )

    def test_quiz_home_redirects_to_first_course_with_questions(self):
        """Verify quiz home redirects to the first course that has quiz data."""
        response = self.client.get(reverse("questions"))
        self.assertEqual(response.status_code, 302)

    def test_course_quiz_page_loads(self):
        """Verify the quiz page for a valid course renders successfully."""
        response = self.client.get(
            reverse("course_quiz", kwargs={"course_id": self.course.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.quiz_one.question)

    def test_invalid_course_quiz_returns_404(self):
        """Verify requesting a non-existent course quiz returns 404."""
        response = self.client.get(
            reverse("course_quiz", kwargs={"course_id": 9999})
        )
        self.assertEqual(response.status_code, 404)

    def test_course_quiz_only_shows_questions_for_selected_course(self):
        """Verify a course quiz page only includes questions for that course."""
        response = self.client.get(
            reverse("course_quiz", kwargs={"course_id": self.course.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.quiz_one.question)
        self.assertNotContains(response, self.quiz_two.question)

    def test_course_quiz_shows_empty_state_for_course_without_questions(self):
        """Verify the empty-state message is shown when no questions exist."""
        response = self.client.get(
            reverse("course_quiz", kwargs={"course_id": self.empty_course.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No quiz questions available")