from drf_yasg import openapi

login_operation_description = '기능\n' \
                              '- 로그인\n' \
                              '- 현재 아이디/비밀번호 입력에 맞는 유저 정보 반환\n' \
                              '\n권한\n' \
                              '- 로그인하지 않은 사용자\n' \
                              '\nrequest body\n' \
                              '- email(필수)\n' \
                              '- password(필수)\n' \
                              '\nresponses\n' \
                              '- 201: 로그인 완료\n' \
                              '- 400: 로그인 실패'

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
