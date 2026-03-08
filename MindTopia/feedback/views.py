"""Views for the feedback app."""

from django.shortcuts import render

from .forms import FeedbackForm


def feed(request):
    """Display and process the feedback form."""
    form = FeedbackForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        feedback = form.save(commit=False)
        if request.user.is_authenticated:
            feedback.user = request.user
        feedback.save()

    return render(request, 'feedback.html', {'form': form})
