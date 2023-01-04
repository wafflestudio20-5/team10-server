from rest_framework import permissions
from authentication.models import User


class DoesUserMatchRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs['pk']
        if request.user == User.objects.get(id=user_id):
            return True
        return False


class IsAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.student_id is not None)
