from django.db import models
from django.contrib.auth.models import User
from instructors.models import Instructor

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default='insert')
    logo = models.ImageField(upload_to="course", default='default.jpg', blank=True)
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses'
    )
    video = models.FileField(upload_to="course", null=True, blank=True)
    pdf = models.FileField(upload_to="course", null=True, blank=True)
    url = models.CharField(max_length=255, default="#")

    def __str__(self):
        return self.title


class CourseFeedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="feedback")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username} on {self.course.title}"