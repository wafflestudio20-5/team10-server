from rest_framework import permissions
from .models import User


# 현재 요청을 날린 유저가 접근하고자 하는 유저 정보가 본인의 정보인지 확인
class DoesUserMatchRequestOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user_id = view.kwargs['pk']
        if request.user == User.objects.get(id=user_id):
            return True
        return False


class IsQualified(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.username is not None and request.user.student_id is not None)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser
