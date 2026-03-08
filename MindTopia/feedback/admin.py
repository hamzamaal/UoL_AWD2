"""Admin configuration for the feedback application."""

from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Configure how Feedback records appear in the Django admin site."""