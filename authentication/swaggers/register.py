from drf_yasg import openapi

register_operation_description = '기능\n' \
                                 '- 회원가입\n' \
                                 '-request body를 토대로 계정 생성\n' \
                                 '- 회원가입 성공 시, 방금 생성된 계정 정보를 반환\n' \
                                 '\n권한\n' \
                                 '- 관리자 계정\n' \
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
