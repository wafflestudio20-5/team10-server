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

change_password_operation_description = '기능\n' \
                                        '- 현재 접속한 유저의 비밀번호를 변경합니다.\n' \
                                        '\n권한\n' \
                                        '- 로그인된 사용자\n' \
                                        '\nrequest body\n' \
                                        '- new_password(필수)\n' \
                                        '\nresponses\n' \
                                        '- 201: 비밀번호 변경 성공\n' \
                                        '- 400: 비밀번호 변경 실패'

logout_request = {

}

logout_responses = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        description='로그아웃이 잘 되었다면, 아무것도 반환하지 않습니다.'
    )
}

logout_operation_description = '기능\n' \
                               '- 로그아웃\n' \
                               '- 현재 로그인된 유저의 토큰을 삭제\n' \
                               '\n권한\n' \
                               '- 로그인된 사용자\n' \
                               '\nrequest body\n' \
                               '- 없음\n' \
                               '\nresponses\n' \
                               '- 200: 로그아웃 성공'

delete_student_operation_description = '기능\n' \
                                       '- 자퇴 신청\n' \
                                       '- 현재 유저를 삭제\n' \
                                       '- URL의 {id]는 삭제하려는 사용자의 id를 의미\n' \
                                       '\n권한\n' \
                                       '- admin 계정\n' \
                                       '- 현재 DELETE 요청을 넣는 유저의 id가 URL의 {id}와 일치(즉, 자퇴 신청을 하는 것이 본인일 때)\n' \
                                       '\nrequest body\n' \
                                       '- 없음\n' \
                                       '\nresponses\n' \
                                       '- 204: 유저 삭제 성공'

register_operation_description = '기능\n' \
                                 '- 회원가입\n' \
                                 '-request body를 토대로 계정 생성\n' \
                                 '- 회원가입 성공 시, 방금 생성된 계정 정보를 반환\n' \
                                 '\n권한\n' \
                                 '- 로그인하지 않은 사용자\n' \
                                 '\nrequest body\n' \
                                 '- email(필수)\n' \
                                 '- password(필수)\n' \
                                 '- username(필수)\n' \
                                 '- student_id(필수)\n' \
                                 '- is_professor(필수, 이 값애 따라 학생/교수 회원가입 구분)\n' \
                                 '\nresponses\n' \
                                 '- 201: 회원가입 성공\n' \
                                 '- 400: 회원가입 실패'

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
    ),
    400: openapi.Schema(
        'Fail',
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='1. 이미 존재하는 이메일일 때, "user with this email already exists." 메시지 반환'
                )
            ),
            'password': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='1. 비밀번호가 8자 미만일 때, "This password is too short. It must contain at least 8 characters." 메시지 반환\n'
                                '2. 비밀번호가 너무 흔할 때, "This password is too common." 메시지 반환'
                )
            ),
            'student_id': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='1. 학번의 길이가 10글자가 아닐 때, "student_id should be 10 length" 메시지 반환\n'
                                '2. 5번째 글자가 "-"가 아닐 때, "student_id form should be XXXX-XXXXX" 메시지 반환\n'
                                '3. 이미 존재하는 학번일 때, "already existing student_id" 메시지 반환\n'
                                '정규표현식으로 숫자 형식만이 입력되게는 제한을 걸어두지 않았습니다.'
                )
            )
        },
        description='필수 값을 넣지 않았을 때 발생하는 400 에러는 작성하지 않았습니다.'
    )
}

idcheck_operation_description = '기능\n' \
                                '- 회원가입 시, 아이디 중복 확인.\n' \
                                '- 현재 가입하려는 이메일이 이미 존재하는 이메일인지 확인.\n' \
                                '\n권한\n' \
                                '- 로그인하지 않은 사용자\n' \
                                '\nrequest body\n' \
                                '- email(필수)\n' \
                                '\nresponses\n' \
                                '- 201: 계정으로 사용할 수 있는 이메일\n' \
                                '- 400: 계정으로 사용할 수 없는 이메일'

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
