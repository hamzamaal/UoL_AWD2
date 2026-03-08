"""Admin configuration for the instructors application."""

from django.contrib import admin

from .models import Instructor


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    """Register the Instructor model in the Django admin interface."""