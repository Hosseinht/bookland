from rest_framework import permissions


class IsAdminOrAuthenticatedUserOrReadOnly(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            # Check permissions for read-only request
            return True
        else:
            # Check permissions for write request
            return obj.user == request.user or request.user.is_staff


class CurrentUserOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_staff or obj.user == user.pk
