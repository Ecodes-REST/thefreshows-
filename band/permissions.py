from.models import Member
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class IsClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj is None:
            return False
        return obj.user_id == request.user.id

class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj is None:
            return False
        return obj.user_id == request.user.id

class ViewClientHistoryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('band.view_history')