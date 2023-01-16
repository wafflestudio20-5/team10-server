from drf_yasg import openapi


login_request_body = openapi.Schema(
    'Login',
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema('email', type=openapi.TYPE_STRING),
        'password': openapi.Schema('password', type=openapi.TYPE_STRING),
    },
    description='로그인을 위해 유저의 이메일과 비밀번호를 입력합니다.'
)

login_responses = {
    201: openapi.Schema(
        'UserDetail',
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema('user id', read_only=True, type=openapi.TYPE_INTEGER),
            'email': openapi.Schema('email', type=openapi.TYPE_STRING),
            'username': openapi.Schema('user name', type=openapi.TYPE_STRING),
            'student_id': openapi.Schema('student_id', type=openapi.TYPE_STRING),
            'is_professor': openapi.Schema('whether current user is professor', type=openapi.TYPE_BOOLEAN),
            'is_superuser': openapi.Schema('whether current user is admin', type=openapi.TYPE_BOOLEAN),
            'classes': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    'Class',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema('class id', read_only=True, type=openapi.TYPE_INTEGER),
                        'name': openapi.Schema('class name', type=openapi.TYPE_STRING),
                    }
                )
            ),
            'token': openapi.Schema('token', type=openapi.TYPE_STRING)
        },
        description='로그인한 유저의 정보를 반환합니다. 유저의 기본적인 정보(유저 id, 이름, 학번, 교수인지, 관리자인지)와 유저가 '
                    '신청한 수업을 list에 담아 받을 수 있습니다. 유저의 token 또한 가져옵니다.'
    ),
    400: openapi.Schema(
        'Error',
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
                default='email or password is not correct',
            )
        },
        description='아이디 혹은 비밀번호 입력이 잘못되었을 때 발생하는 오류입니다.'
    ),
}

change_password_operation_description = 'request body로 new_password를 입력받습니다. ' \
                                        'Token을 이용해 현재 요청을 넣은 유저를 알아내고, 현재 유저의 ' \
                                        'password를 new_password로 변경합니다. 이 때, 이전 비밀번호와 new_password가 ' \
                                        '동일하다면 오류가 발생합니다.'

change_password_responses = {
    201: openapi.Schema(
        'ChangePassword',
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(
                type=openapi.TYPE_STRING,
                default="new password has been set"
            )
        },
        description='비밀번호 변경이 성공했다면, 이 response가 반환됩니다.'
    ),
    400: openapi.Schema(
        'Error',
        type=openapi.TYPE_OBJECT,
        properties={
            'error': openapi.Schema(
                type=openapi.TYPE_STRING,
            )
        },
        description='new_password가 8자 미만이거나, 비밀번호가 이전 비밀번호와 동일하다면, 이 response가 반환됩니다.'
                    '\n1. 8자 이하일 때, "too short password. password length should be >=8."'
                    '\n2. 이전 비밀번호와 동일할 때, "same with previous password."'
                    '\n3. 그 외 기타 사유.'
    ),
}

logout_request = {

}

logout_responses = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='로그아웃이 잘 되었다면, 아무것도 반환하지 않습니다.'
    )
}
