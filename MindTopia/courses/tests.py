from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from instructors.models import Instructor
from .models import Course, CourseFeedback


class CourseViewAndApiTests(TestCase):
    def setUp(self):
        # Django test client for normal Django views
        self.web_client = Client()

        # DRF client for API endpoints
        self.api_client = APIClient()

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

        self.student_user = User.objects.create_user(
            username='student1',
            password='TestPass123'
        )
        self.student_user.userprofile.role = 'student'
        self.student_user.userprofile.save()

        self.teacher_user = User.objects.create_user(
            username='teacher1',
            password='TestPass123'
        )
        self.teacher_user.userprofile.role = 'teacher'
        self.teacher_user.userprofile.save()

    def test_courses_page_loads(self):
        response = self.web_client.get(reverse('courses'))
        self.assertEqual(response.status_code, 200)

    def test_course_detail_requires_login(self):
        response = self.web_client.get(reverse('course_detail', kwargs={'course_id': self.course.id}))
        self.assertEqual(response.status_code, 302)

    def test_student_can_register_for_course(self):
        self.web_client.login(username='student1', password='TestPass123')
        response = self.web_client.get(reverse('register_course', kwargs={'course_id': self.course.id}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.student_user.userprofile.registered_courses.filter(id=self.course.id).exists())

    def test_teacher_cannot_register_for_course(self):
        self.web_client.login(username='teacher1', password='TestPass123')
        response = self.web_client.get(reverse('register_course', kwargs={'course_id': self.course.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.teacher_user.userprofile.registered_courses.filter(id=self.course.id).exists())

    def test_submit_feedback_creates_feedback(self):
        self.web_client.login(username='student1', password='TestPass123')
        response = self.web_client.post(reverse('submit_feedback', kwargs={'course_id': self.course.id}), {
            'comment': 'Very helpful course',
            'rating': 5,
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CourseFeedback.objects.filter(course=self.course, user=self.student_user).exists())

    def test_api_courses_is_public(self):
        response = self.api_client.get(reverse('api_courses'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Basics')

    def test_api_course_detail_is_public(self):
        response = self.api_client.get(reverse('api_course_detail', kwargs={'pk': self.course.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Python Basics')

    def test_api_course_feedback_denies_unauthenticated(self):
        response = self.api_client.get(reverse('api_course_feedback', kwargs={'course_id': self.course.id}))
        self.assertEqual(response.status_code, 403)

    def test_api_course_feedback_denies_student(self):
        CourseFeedback.objects.create(
            course=self.course,
            user=self.student_user,
            comment='Great',
            rating=5
        )
        self.api_client.force_authenticate(user=self.student_user)
        response = self.api_client.get(reverse('api_course_feedback', kwargs={'course_id': self.course.id}))
        self.assertEqual(response.status_code, 403)

    def test_api_course_feedback_allows_teacher(self):
        CourseFeedback.objects.create(
            course=self.course,
            user=self.student_user,
            comment='Great',
            rating=5
        )
        self.api_client.force_authenticate(user=self.teacher_user)
        response = self.api_client.get(reverse('api_course_feedback', kwargs={'course_id': self.course.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['comment'], 'Great')