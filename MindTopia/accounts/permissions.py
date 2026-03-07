from rest_framework.permissions import BasePermission


class IsTeacherUser(BasePermission):
    """
    Allows access only to authenticated users whose profile role is 'teacher'.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'userprofile')
            and request.user.userprofile.role == 'teacher'
        )