"""Views for account management and teacher-restricted API access."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework import generics

from .forms import ProfileUpdateForm, StatusUpdateForm, UserRegisterForm, UserUpdateForm
from .models import UserProfile
from .permissions import IsTeacherUser
from .serializers import UserProfileSerializer, UserSerializer


def register(request):
    """Register a new user account and associated profile."""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Account created successfully! You can now log in.",
            )
            return redirect("login")
    else:
        form = UserRegisterForm()

    return render(request, "register.html", {"form": form})


@login_required
def profile(request):
    """Display the logged-in user's profile page."""
    return render(request, "accounts/profile.html")


@login_required
def profile_update(request):
    """Update user account and profile information."""
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.userprofile,
        )

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(
                request,
                "Your profile has been updated successfully!",
            )
            return redirect(reverse("profile"))
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {"u_form": u_form, "p_form": p_form}
    return render(request, "accounts/profile_update.html", context)


def is_teacher(user):
    """Return True if the user has the teacher role."""
    return hasattr(user, "userprofile") and user.userprofile.role == "teacher"


@user_passes_test(is_teacher)
def teacher_dashboard(request):
    """Allow teachers to search and view student profiles."""
    query = request.GET.get("q", "")
    users = UserProfile.objects.filter(role="student").select_related("user")

    if query:
        users = users.filter(
            Q(user__username__icontains=query)
            | Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
        )

    context = {"users": users, "query": query}
    return render(request, "accounts/teacher_dashboard.html", context)


@login_required
def user_home(request, username=None, *args, **kwargs):
    """Display a user's home page, status update form, and related users."""
    if username:
        profile_obj = get_object_or_404(UserProfile, user__username=username)
    else:
        profile_obj = request.user.userprofile

    if request.method == "POST":
        form = StatusUpdateForm(request.POST, instance=profile_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Status updated successfully!")
            return redirect(
                "user_home_username",
                username=profile_obj.user.username,
            )
    else:
        form = StatusUpdateForm(instance=profile_obj)

    context = {
        "user": profile_obj,
        "form": form,
        "all_users": UserProfile.objects.exclude(user=request.user),
    }
    return render(request, "accounts/user_home.html", context)


class UserListView(generics.ListAPIView):
    """Return a teacher-only list of all users."""

    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
    permission_classes = [IsTeacherUser]


class StudentListView(generics.ListAPIView):
    """Return a teacher-only list of student profiles."""

    queryset = (
        UserProfile.objects.filter(role="student")
        .select_related("user")
        .order_by("user__username")
    )
    serializer_class = UserProfileSerializer
    permission_classes = [IsTeacherUser]


class UserProfileDetailView(generics.RetrieveAPIView):
    """Return details for a specific user profile (teacher access only)."""

    serializer_class = UserProfileSerializer
    permission_classes = [IsTeacherUser]

    def get_object(self):
        """Retrieve the requested profile using the username parameter."""
        username = self.kwargs["username"]
        return get_object_or_404(
            UserProfile.objects.select_related("user"),
            user__username=username,
        )