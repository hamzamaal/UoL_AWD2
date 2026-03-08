"""Admin configuration for the accounts app."""

from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Display user profile details in the Django admin site."""

    list_display = ('user', 'get_first_name', 'get_last_name', 'role', 'image')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'role')

    @staticmethod
    def get_first_name(obj):
        """Return the related user's first name for admin display."""
        return obj.user.first_name

    get_first_name.short_description = 'First Name'

    @staticmethod
    def get_last_name(obj):
        """Return the related user's last name for admin display."""
        return obj.user.last_name

    get_last_name.short_description = 'Last Name'
