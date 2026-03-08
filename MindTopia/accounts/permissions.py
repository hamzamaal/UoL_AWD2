"""Custom DRF permission classes for the accounts application.

This module defines permission rules used by Django Rest Framework
to control access to protected API endpoints.
"""

from rest_framework.permissions import BasePermission


class IsTeacherUser(BasePermission):
    """
    Permission class that allows access only to authenticated teachers.

    This permission ensures that the requesting user:
    - is authenticated
    - has an associated UserProfile
    - has the role 'teacher'
    """

    def has_permission(self, request, view):
        """
        Determine whether the current request should be permitted.

        Returns True only if the user is logged in and their associated
        UserProfile has the role set to 'teacher'.
        """

        # Ensure the request contains a valid authenticated user
        return (
            bool(request.user)
            and request.user.is_authenticated
            # Confirm the user has an associated profile
            and hasattr(request.user, "userprofile")
            # Restrict access to users with the teacher role
            and request.user.userprofile.role == "teacher"
        )