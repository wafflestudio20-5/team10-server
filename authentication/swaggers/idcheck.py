from drf_yasg import openapi

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
