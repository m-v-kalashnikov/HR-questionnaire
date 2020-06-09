from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerProfileOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        try:
            return obj.user == request.user
        except AttributeError:
            return False


class IsOwnerProfileOrManagerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.profile.is_manager
