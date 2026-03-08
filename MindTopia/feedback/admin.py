"""Admin configuration for the feedback app."""

from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Register the Feedback model in the Django admin interface."""