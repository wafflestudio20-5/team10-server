from drf_yasg import openapi

class_user_list_operation_description = '기능\n' \
                                        '- 특정 수업을 듣고 있는 수강생 리스트를 반환\n' \
                                        '- URL의 {id}에는 수업의 id가 들어갑니다.\n' \
                                        '\npermission\n' \
                                        '- admin 계정\n' \
                                        '- 로그인하고, 개인정보 세팅이 모두 완료된 사용자\n' \
                                        '\nrequest body\n' \
                                        '- 아무것도 없습니다.\n' \
                                        '\nresponses\n' \
                                        '- 200: 특정 수업의 수강생 리스트 반환 성공\n' \
                                        '\n비고\n' \
                                        '- 용이한 pagination 테스트를 위해, 한 번에 2명씩 수강생 정보를 가져옵니다.\n' \
                                        '- pagination 정렬 순서는 username 사전순입니다.'

class_user_list_responses = {
    200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'next': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='다음 2명의 수강생을 불러올 api 주소를 담고 있습니다.\n'
                            '만약 현재 불러온 수강생들이 마지막이라면, null 값을 갖습니다.',
            ),
            'previous': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='이전 2명의 수강생을 불러올 api 주소를 담고 있습니다.\n'
                            '처음 수강생을 불러왔을 때는, 이전 2명의 수강생이 없으므로 null 값을 갖습니다.',
            ),
            'results': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    'User',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            read_only=True,
                        ),
                        'username': openapi.Schema(
                            type=openapi.TYPE_STRING,
                        ),
                        'student_id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                        ),
                        'is_professor': openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                        ),
                    }
                )
            )
        }
    )
}
