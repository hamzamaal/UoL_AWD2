"""Admin configuration for the accounts application."""

from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Configure how user profiles are displayed in the Django admin."""

    # Fields shown in the admin list view for each user profile.
    list_display = ("user", "get_first_name", "get_last_name", "role", "image")

    # Fields searchable from the admin search bar.
    search_fields = ("user__username", "user__first_name", "user__last_name", "role")

    @staticmethod
    def get_first_name(obj):
        """Return the related user's first name for display in the admin."""
        return obj.user.first_name

    get_first_name.short_description = "First Name"

    @staticmethod
    def get_last_name(obj):
        """Return the related user's last name for display in the admin."""
        return obj.user.last_name

    get_last_name.short_description = "Last Name"