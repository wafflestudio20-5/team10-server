from drf_yasg import openapi


login_request_body = openapi.Schema(
    'Login',
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema('email', type=openapi.TYPE_STRING),
        'password': openapi.Schema('password', type=openapi.TYPE_STRING),
    },
    description='로그인을 위해 유저의 이메일과 비밀번호 입력'
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
        description='로그인한 유저의 정보 반환'
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
        description='로그인 입력이 잘못되었을 때 발생하는 오류'
    ),
}

