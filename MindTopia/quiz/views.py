from django.shortcuts import render, get_object_or_404
from quiz.models import Quiz
from courses.models import Course

def qpage(request, course_id):
	course = get_object_or_404(Course, id=course_id)
	questions = Quiz.objects.filter(course=course)

	return render(request, 'quiz.html', { 'questions': questions, 'course': course})