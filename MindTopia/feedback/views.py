from django.shortcuts import render
from .forms import feedbackForm
# Create your views here.
def feed(request):
	template="feedback.html"

	if request.method == "POST":
		form = feedbackForm(request.POST)

		if form.is_valid():
			feedback = form.save(commit=False)
			if request.user.is_authenticated:
				feedback.user = request.user
			feedback.save()

	else:
		form = feedbackForm()

	context = {
		'form' : form ,
	}			

	return render(request, template, context)