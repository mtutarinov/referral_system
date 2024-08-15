from rest_framework import permissions


class CustomPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            pass

    def has_object_permission(self, request, view, obj):
        pass
