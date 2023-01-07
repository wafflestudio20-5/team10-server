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
# 기존 IsAuthenticated 는 개인정보가 설정되었는지 확인해주지 않으므로, IsAuthenticated 보다는 IsQualified 를 사용하기를 장려함.
class IsQualified(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user.is_authenticated and request.user.username is not None and request.user.student_id is not None)


# 현재 요청을 날린 유저가 관리자이지 확인
# 기존 Django rest framework 의 IsAdmin 은 user.is_staff = True 를 검사하는데, 해당 부분보다는 is_superuser 값을 참조하는 것이 옳을 것 같아 정의함.
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


# 현재 요청을 날린 유저가 교수인지 확인
# 현재 요청이 안전한 요청이라면 허용, 안전하지 않은 요청이라면 교수에게만 권한 허용
class IsProfessorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user.is_authenticated and request.user.username is not None and request.user.is_professor)


# 현재 요청이 안전한 요청이라면 허용, 안전하지 않은 요청이라만 만든 사람에게만 권한 허용
class IsCreatorReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.created_by == request.user
