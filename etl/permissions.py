from rest_framework import permissions
from authentication.models import User


# 현재 요청을 날린 유저가 접근하고자 하는 유저 정보가 본인의 정보인지 확인
class DoesUserMatchRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        user_id = view.kwargs['pk']
        if request.user == User.objects.get(id=user_id):
            return True
        return False


# 현재 요청을 날린 유저가 개인정보(이름, 학번) 설정이 완료되어 etl의 서비스에 접근할 수 있는지 확인
# 프론트엔드 단에서 username==null or student_id==null 조건문을 통해 적절히 분기하겠지만, 백엔드 단에서 한 번 더 확인해주기 위함.
class IsQualified(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_authenticated and request.user.username_validator is not None and request.user.student_id is not None)
