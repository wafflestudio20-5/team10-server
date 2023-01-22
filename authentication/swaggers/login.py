from drf_yasg import openapi

login_operation_description = '기능\n' \
                              '- 로그인\n' \
                              '- 현재 아이디/비밀번호 입력에 맞는 유저 id와 토큰 반환\n' \
                              '- 유저 id와 토큰만 반환하므로, 해당 정보를 바탕으로 유저 정보를 GET하는 요청을 보내주세요.\n' \
                              '\n권한\n' \
                              '- 관리자 계정\n' \
                              '- 로그인하지 않은 사용자\n' \
                              '\nrequest body\n' \
                              '- email(필수)\n' \
                              '- password(필수)\n' \
                              '\nresponses\n' \
                              '- 200: 로그인 완료\n' \
                              '- 400: 로그인 실패\n' \
                              '\n비고\n' \
                              '- 로그인을 통해 얻어온 access token은 Header에 key=Authorization, value=Bearer ${access_token}과 ' \
                              '같이 담아서 이후 요청에 보내주시면 됩니다.'

login_request_body = openapi.Schema(
    'Login',
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema('email', type=openapi.TYPE_STRING),
        'password': openapi.Schema('password', type=openapi.TYPE_STRING),
    },
    description='로그인을 위해 유저의 이메일과 비밀번호를 입력합니다.'
)
