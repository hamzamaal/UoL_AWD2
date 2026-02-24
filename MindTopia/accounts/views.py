from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User  #  FIXED: Import User model
from django.db.models import Q  #  FIXED: Import Q for advanced search queries
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, StatusUpdateForm


#  User Registration View
def register(request):
    """Handles user registration with default role as student"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, role='student')
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    """Displays the user's profile page"""
    return render(request, 'accounts/profile.html')  # ✅ Ensure this matches the template path



@login_required
def profile_update(request):
    """Allows users to update their profile information"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect(reverse('profile'))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    return render(request, 'accounts/profile_update.html', {'u_form': u_form, 'p_form': p_form})


#  Check if user is a teacher
def is_teacher(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'teacher'


@user_passes_test(is_teacher)
def teacher_dashboard(request):
    """Allows teachers to search for students and other teachers"""
    
    query = request.GET.get('q', '')  # Get the search query from the request
    users = UserProfile.objects.all()  # Default: Show all users

    if query:
        users = users.filter(
            Q(user__username__icontains=query) |  # Search by username
            Q(first_name__icontains=query) |  # Search by first name
            Q(last_name__icontains=query) |  # Search by last name
            Q(role__icontains=query)  # Search by role (e.g., "student" or "teacher")
        )

    return render(request, 'accounts/teacher_dashboard.html', {
        'users': users,
        'query': query
    })


@login_required
def user_home(request, username=None, *args, **kwargs):
    """Displays a user's home page with status updates & courses."""
    if username:
        user = get_object_or_404(UserProfile, user__username=username)
    else:
        user = request.user.userprofile

    if request.method == "POST":
        form = StatusUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Status updated successfully!")
            return redirect("user_home_username", username=user.user.username)
    else:
        form = StatusUpdateForm(instance=user)

    all_users = UserProfile.objects.exclude(user=request.user)

    return render(request, 'accounts/user_home.html', {
        'user': user,
        'form': form,
        'all_users': all_users,
    })



#  API View to List All Users
class UserListView(generics.ListAPIView):
    """Returns a list of all users (Requires Authentication)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Ensures only logged-in users can access


#  API View to Retrieve a Specific UserProfile
class UserProfileDetailView(generics.RetrieveAPIView):
    """Retrieve a user's profile by username"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'user__username'  # Allows lookup via username
