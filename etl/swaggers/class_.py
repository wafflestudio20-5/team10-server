from drf_yasg import openapi

# TODO: 페이지네이션 적용 후 비고 삭제
class_get_operation_description = '기능\n' \
                                  '- 모든 존재하는 수업 목록을 불러옵니다.\n' \
                                  '\n권한\n' \
                                  '- admin 계정\n' \
                                  '- 로그인한 사용자\n' \
                                  '\nrequest body\n' \
                                  '- 아무것도 없습니다.\n' \
                                  '\nresponses\n' \
                                  '- 200: 모든 수업 목록 받아오기 성공\n' \
                                  '\n비고\n' \
                                  '- 아직 pagination을 적용하지 않았습니다.'

class_post_operation_description = '기능\n' \
                                   '- 수업 하나를 생성합니다.\n' \
                                   '\npermission\n' \
                                   '- admin 계정\n' \
                                   '- 로그인하고, 교수인 사용자\n' \
                                   '\nrequest body\n' \
                                   '- 수업 이름(필수)\n' \
                                   '\nresponses\n' \
                                   '- 201: 수업 하나 생성 성공'

class_post_request_body = openapi.Schema(
    'Class',
    type=openapi.TYPE_OBJECT,
    required=['name'],
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING)
    }
)

class_post_responses = {
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

class_delete_operation_description = '기능\n' \
                                     '- 수업 하나 삭제\n' \
                                     '- URL의 {id}는 삭제할 수업의 id 값이 들어갑니다.\n' \
                                     '\npermission\n' \
                                     '- admin 계정\n' \
                                     '- 해당 수업을 생성한 사용자\n' \
                                     '\nrequest body\n' \
                                     '- 아무것도 없습니다.\n' \
                                     '\nresponses\n' \
                                     '- 204: 수업 하나 삭제 성공'
