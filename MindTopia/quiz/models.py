from django.db import models
from courses.models import Course

# Create your models here.
class Quiz(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='quiz_questions', null=True, blank=True)
	question = models.CharField(max_length = 500)
	option1 = models.CharField(max_length = 20)
	option2 = models.CharField(max_length = 20)
	option3 = models.CharField(max_length = 20)
	option4 = models.CharField(max_length = 20)
	answer = models.CharField(max_length = 20)