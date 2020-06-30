from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOrMeCanEdit(BasePermission):
    def has_object_permission(self, request, view, obj=None):
        """Only the user can modify existing instances."""
        is_safe = request.method in SAFE_METHODS

        try:
            is_user = request.user == obj
        except AttributeError:
            is_user = False

        return is_safe or is_user or request.user.is_superuser
