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

change_password_request = openapi.Schema(
    'ChangePassword',
    type=openapi.TYPE_OBJECT,
    required=['new_password'],
    properties={
        'new_password': openapi.Schema(
            type=openapi.TYPE_STRING,
            min_length=8,
        )
    },
    description='새롭게 설정할 비밀번호를 request body에 담습니다.'
)

change_password_responses = {
    201: openapi.Schema(
        'Success',
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
                    '\n1. 8자 미만일 때, "too short password. password length should be >=8."'
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

logout_operation_description = '현재 유저의 토큰을 삭제합니다. request body로 아무것도 받지 않습니다.\n' \
                               '로그아웃이 잘 되어 토큰이 삭제되었다면, ' \
                               '200 status code를 반환합니다.'

delete_student_operation_description = '자퇴 신청에 사용합니다. 학생의 정보를 삭제합니다. request body로 아무것도 받지 않습니다.\n' \
                                       '{id}는 학생의 id를 의미합니다.' \
                                 '잘 삭제되었다면, 204 status code를 반환합니다.'

register_operation_description = '일반 회원가입 시, email, password, username, student_id, is_professor를' \
                                 ' 모두 입력으로 받습니다.\n"is_professor": false 일 경우 학생 회원가입, ' \
                                 '"is_professor": true 일 경우 교수 회원가입입니다.\n회원가입이 잘 처리되었다면 ' \
                                 '현재 생성된 유저 정보를 다시 돌려받습니다.'

register_responses = {
    201: openapi.Schema(
        'Success',
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER, read_only=True
            ),
            'email': openapi.Schema(
                type=openapi.TYPE_STRING
            ),
            'username': openapi.Schema(
                type=openapi.TYPE_STRING
            ),
            'student_id': openapi.Schema(
                type=openapi.TYPE_STRING
            ),
            'is_professor': openapi.Schema(
                type=openapi.TYPE_BOOLEAN
            )
        }
    )
}

idcheck_operation_description = '아이디 중복확인을 위한 API입니다. 현재 유저가 생성하려는 이메일이 이미 존재하는' \
                                ' 이메일인지 확인해줍니다.\nrequest body에 email 값을 받습니다.'

idcheck_operation_responses = {
    201: openapi.Schema(
        'Success',
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, default='valid')
        },
        description='이미 존재하는 이메일이 아닌 경우, 이 response를 반환합니다.'
    ),
    400: openapi.Schema(
        'Fail',
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='1. 적절한 이메일 형식이 아니라면, "Enter a valid email address." 메시지 반환.\n'
                                '2. 이미 존재하는 이메일이라면, "This field must be unique." 메시지 반환.'
                ),
            ),
        }
    )
}