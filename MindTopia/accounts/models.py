from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from courses.models import Course


class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # Status updates
    status_update = models.TextField(blank=True, null=True, help_text="Share your latest update!")

    # Registered courses for students
    registered_courses = models.ManyToManyField(Course, blank=True, related_name="students")

    # For teachers only: Track students they are responsible for
    students = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name="teacher_students"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
