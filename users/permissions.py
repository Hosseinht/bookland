from rest_framework import permissions


class IsAdminUserOrAnonymous(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and not request.user.is_staff:
            return False
        else:
            return True
