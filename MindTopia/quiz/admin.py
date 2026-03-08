"""Admin configuration for the quiz app."""

from django.contrib import admin

from .models import Quiz


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Display quiz questions in the Django admin interface."""

    list_display = ('question', 'course')
    search_fields = ('question', 'course__title')
