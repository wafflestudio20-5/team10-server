from drf_yasg import openapi

class_professor_get_operation_description = '기능\n' \
                                            '- 현재 사용자가 생성한 수업 리스트 조회\n' \
                                            '\npermission\n' \
                                            '- admin 계정\n' \
                                            '- 로그인하고, 개인정보를 모두 세팅했고, 교수인 사용자\n' \
                                            '\nrequest body\n' \
                                            '- 아무것도 없습니다.\n' \
                                            '\nresponses\n' \
                                            '- 200: 수업 리스트 조회 성공'

class_professor_post_operation_description = '기능\n' \
                                             '- 수업 생성\n' \
                                             '\npermission\n' \
                                             '- admin 계정\n' \
                                             '- 로그인하고, 개인정보를 모두 세팅했고, 교수인 사용자\n' \
                                             '\nrequest body\n' \
                                             '- name(필수)\n' \
                                             '\nresponses\n' \
                                             '- 201: 수업 생성 성공\n' \
                                             '\n비고\n' \
                                             '- 사실 /etl/class/에 POST 요청을 넣는 것과 동작이 동일합니다.'

class_professor_post_responses = {
    201: openapi.Schema(
        'Class',
        type=openapi.TYPE_OBJECT,
        description='방금 생성된 수업 정보를 반환합니다.',
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                read_only=True,
            ),
            'name': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='수업 이름',
            ),
            'created_by': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='수업을 생성한 사람의 정보. 생성한 사람의 이름만 반환합니다.',
                properties={
                    'username': openapi.Schema(
                        type=openapi.TYPE_STRING,
                    ),
                }
            )
        }
    )
}
