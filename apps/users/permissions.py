from rest_framework.permissions import BasePermission


class IsProfileOwnerOrAdmin(BasePermission):
    """
    Permission to access the profile only to the owner or administrator.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.role == 'admin'