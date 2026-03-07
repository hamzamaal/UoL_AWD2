# Import Django's built-in admin module used to register models in the admin interface
from django.contrib import admin

# Import the UserProfile model from the current application's models
from .models import UserProfile

# Register the UserProfile model with the Django admin site using a decorator
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    # Specify which fields should be displayed in the admin list view for UserProfile records
    list_display = ('user', 'first_name', 'last_name', 'role', 'image')