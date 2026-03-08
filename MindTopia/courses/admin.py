"""Admin configuration for the courses app."""

from django.contrib import admin

from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Display course records in the Django admin site."""

    list_display = ('title', 'instructor', 'url')
    search_fields = ('title', 'instructor__name')
