"""Admin configuration for the quiz application."""

from django.contrib import admin

from .models import Quiz


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Configure how quiz questions are displayed in the admin interface."""

    list_display = ("question", "course")
    search_fields = ("question", "course__title")
    list_filter = ("course",)