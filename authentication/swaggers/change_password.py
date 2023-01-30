from drf_yasg import openapi

change_password_operation_description = '기능\n' \
                                        '- 현재 접속한 유저의 비밀번호를 변경합니다.\n' \
                                        '\n권한\n' \
                                        '- 로그인된 사용자\n' \
                                        '\nrequest body\n' \
                                        '- new_password(필수)\n' \
                                        '\nresponses\n' \
                                        '- 201: 비밀번호 변경 성공\n' \
                                        '- 400: 비밀번호 변경 실패'

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
