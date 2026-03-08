"""Custom DRF permissions for the accounts app."""

from rest_framework.permissions import BasePermission


class IsTeacherUser(BasePermission):
    """Allow access only to authenticated users with the teacher role."""

    def has_permission(self, request, view):
        """Return True when the current user is an authenticated teacher."""
        return (
            bool(request.user)
            and request.user.is_authenticated
            and hasattr(request.user, 'userprofile')
            and request.user.userprofile.role == 'teacher'
        )
