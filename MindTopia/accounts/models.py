# Import Django's model framework used to define database models
from django.db import models

# Import Django's built-in User model for authentication and user accounts
from django.contrib.auth.models import User

# Import PIL (Python Imaging Library) to process and resize uploaded images
from PIL import Image

# Import the Course model to allow users to register for courses
from courses.models import Course


# Define the UserProfile model which extends the default Django User model
class UserProfile(models.Model):

    # Define the possible user roles within the system
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )

    # Create a one-to-one relationship with the Django User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")

    # Store the role of the user (student or teacher)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    # Optional text field allowing users to write a short biography
    bio = models.TextField(max_length=500, blank=True, null=True)

    # Optional field for storing the user's location
    location = models.CharField(max_length=100, blank=True, null=True)

    # Optional field for storing the user's date of birth
    date_of_birth = models.DateField(blank=True, null=True)

    # Field used to upload and store the user's profile image
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    # Field allowing users to post short status updates
    status_update = models.TextField(blank=True, null=True, help_text="Share your latest update!")

    # Many-to-many relationship allowing students to register for multiple courses
    registered_courses = models.ManyToManyField(Course, blank=True, related_name="students")

    # Self-referencing many-to-many relationship used for teachers to track their students
    students = models.ManyToManyField(
        'self', symmetrical=False, blank=True, related_name="teacher_students"
    )

    # Define the string representation of the model when displayed in Django admin or queries
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

    # Override the save method to automatically resize uploaded profile images
    def save(self, *args, **kwargs):

        # Call the original save method to ensure the object is saved before processing the image
        super().save(*args, **kwargs)

        # Open the uploaded profile image using PIL
        img = Image.open(self.image.path)

        # Check if the image dimensions exceed the allowed size
        if img.height > 300 or img.width > 300:

            # Define the maximum allowed image size
            output_size = (300, 300)

            # Resize the image while maintaining its aspect ratio
            img.thumbnail(output_size)

            # Save the resized image back to the original file path
            img.save(self.image.path)
            