from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


class Feedback(models.Model):
	choice = (
					('y', 'Yes'),
					('n', 'No'),
				)
	cc = (
					('a', '1'),
					('b', '2'),
					('c', '3'),
					('d', '4'),
					('e', '5'),
				)

	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	ui = models.CharField("Did you like UI of our website", max_length=30, choices = choice)
	sug = models.TextField("Suggest some changes in the website", default="")
	satisfy = models.CharField("Are you satisfied with course content",  max_length=30, choices = choice)
	sugg = models.TextField("Suggest some changes in course content or any additions", default="")
	rating = models.CharField("Rate your experience", max_length=10, choices = cc)
	
	def __str__(self):
		if self.user:
			return self.user.username
		return "Anonymous Feedback"