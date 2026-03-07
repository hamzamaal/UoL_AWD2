from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, StatusUpdateForm
from .permissions import IsTeacherUser


# User Registration View
def register(request):
    """Handles user registration with default role as student"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})


@login_required
def profile(request):
    """Displays the user's profile page"""
    return render(request, 'accounts/profile.html')


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


# Check if user is a teacher
def is_teacher(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'teacher'


@user_passes_test(is_teacher)
def teacher_dashboard(request):
    """Allows teachers to search for students only"""
    query = request.GET.get('q', '')

    # Only show student profiles
    users = UserProfile.objects.filter(role='student')

    if query:
        users = users.filter(
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query)
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


# API View to List All Users - teacher only
class UserListView(generics.ListAPIView):
    """Returns a list of all users (Teacher access only)"""
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsTeacherUser]


# API View to List Student Profiles Only - teacher only
class StudentListView(generics.ListAPIView):
    """Returns a list of student profiles only (Teacher access only)"""
    queryset = UserProfile.objects.filter(role='student').select_related('user').order_by('user__username')
    serializer_class = UserProfileSerializer
    permission_classes = [IsTeacherUser]


# API View to Retrieve a Specific UserProfile - teacher only
class UserProfileDetailView(generics.RetrieveAPIView):
    """Retrieve a user's profile by username (Teacher access only)"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsTeacherUser]

    def get_object(self):
        username = self.kwargs['username']
        return get_object_or_404(UserProfile.objects.select_related('user'), user__username=username)