from drf_yasg import openapi

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
