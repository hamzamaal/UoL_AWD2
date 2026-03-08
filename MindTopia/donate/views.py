"""Views for the donate app."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def pay(request):
    """Render the donation or payment page for authenticated users."""
    return render(request, 'payment.html')
