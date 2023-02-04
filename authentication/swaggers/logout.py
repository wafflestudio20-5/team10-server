from drf_yasg import openapi


logout_operation_description = '기능\n' \
                               '- 로그아웃\n' \
                               '- 현재 로그인된 유저의 토큰을 삭제\n' \
                               '\n권한\n' \
                               '- 로그인된 사용자\n' \
                               '\nrequest body\n' \
                               '- 없음\n' \
                               '\nresponses\n' \
                               '- 200: 로그아웃 성공\n' \
                               '\n비고\n' \
                               '- jwt 토큰으로 변경 이후 실제 로그아웃이 잘 되는지 잘 모르겠습니다.\n' \
                               'insomnia로 확인했을 때는 되지 않았는데, 프론트엔드 단에서 확인 부탁드립니다.'

logout_responses = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'success': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                default=True,
            )
        }
    )
}
