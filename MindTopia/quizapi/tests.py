from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from instructors.models import Instructor
from courses.models import Course
from quiz.models import Quiz


class QuizApiTests(TestCase):
    def setUp(self):
        self.api_client = APIClient()

        self.user = User.objects.create_user(
            username='student1',
            password='TestPass123'
        )
        self.user.userprofile.role = 'student'
        self.user.userprofile.save()

        self.instructor = Instructor.objects.create(
            name='Instructor One',
            url='#'
        )

        self.course = Course.objects.create(
            title='Python Basics',
            description='Introductory Python course',
            instructor=self.instructor,
            url='#'
        )

        self.empty_course = Course.objects.create(
            title='Empty Course',
            description='No quiz questions yet',
            instructor=self.instructor,
            url='#'
        )

        self.quiz = Quiz.objects.create(
            course=self.course,
            question='What is Python?',
            option1='Snake',
            option2='Programming Language',
            option3='Car',
            option4='Game',
            answer='b'
        )

    def test_quiz_list_api_is_public(self):
        response = self.api_client.get(reverse('api_quiz_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_quiz_detail_api_is_public(self):
        response = self.api_client.get(reverse('api_quiz_detail', kwargs={'pk': self.quiz.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['question'], 'What is Python?')

    def test_quiz_detail_returns_404_for_invalid_quiz(self):
        response = self.api_client.get(reverse('api_quiz_detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_quiz_by_course_api_is_public(self):
        response = self.api_client.get(reverse('api_course_quiz_list', kwargs={'course_id': self.course.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['course'], self.course.id)

    def test_quiz_by_course_returns_empty_list_when_no_questions_exist(self):
        response = self.api_client.get(reverse('api_course_quiz_list', kwargs={'course_id': self.empty_course.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)