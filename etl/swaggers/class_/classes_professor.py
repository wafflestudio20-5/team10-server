from drf_yasg import openapi

classes_professor_get_operation_description = '기능\n' \
                                            '- 현재 사용자가 생성한 수업 리스트 조회\n' \
                                            '- 페이지네이션이 적용되어, 이름 사전 순으로 수업을 10개씩 반환합니다.\n' \
                                            '\npermission\n' \
                                            '- admin 계정\n' \
                                            '- 로그인하고, 개인정보를 모두 세팅했고, 교수인 사용자\n' \
                                            '\nrequest body\n' \
                                            '- 아무것도 없습니다.\n' \
                                            '\nresponses\n' \
                                            '- 200: 수업 리스트 조회 성공' \
                                            '\n사용 예시\n' \
                                            '- 세 번쩨 페이지에 해당하는 수업 목록을 불러오고 싶다면, ' \
                                              '"baseURL/etl/classes/professor/?page=3" GET 요청을 통해 가져올 수 있습니다.' \

classes_professor_get_responses = {
    200: openapi.Schema(
        'Class List',
        type=openapi.TYPE_OBJECT,
        properties={
            'count': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='현재 사용자가 만든 수업의 총 갯수입니다.',
            ),
            'next': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='다음 10개의 수업을 불러올 api 주소를 담고 있습니다.\n'
                            '만약 현재 불러온 수업들이 마지막이라면, null 값을 갖습니다.',
            ),
            'previous': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='이전 10개의 수업을 불러올 api 주소를 담고 있습니다.\n'
                            '처음 수업을 불러왔을 때는, 이전 10개의 수업이 없으므로 null 값을 갖습니다.',
            ),
            'results': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    'Class',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER,
                            read_only=True,
                        ),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='수업 이름입니다',
                        ),
                        'created_by': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'username': openapi.Schema(
                                    type=openapi.TYPE_STRING,
                                )
                            }
                        )
                    }
                )
            ),
        }
    ),
}

classes_professor_get_parameter_page = openapi.Parameter(
    'page',
    openapi.IN_QUERY,
    description='페이지네이션으로 해당하는 페이지를 반환합니다.',
    required=True,
    type=openapi.TYPE_INTEGER,
)

classes_professor_get_manual_parameters = [classes_professor_get_parameter_page]

classes_professor_post_operation_description = '기능\n' \
                                             '- 수업 생성\n' \
                                             '\npermission\n' \
                                             '- admin 계정\n' \
                                             '- 로그인하고, 개인정보를 모두 세팅했고, 교수인 사용자\n' \
                                             '\nrequest body\n' \
                                             '- name(필수)\n' \
                                             '\nresponses\n' \
                                             '- 201: 수업 생성 성공, 생성한 수업 정보 반환.\n' \
                                             '\n비고\n' \
                                             '- 사실 baseURL/etl/classes/에 POST 요청을 넣는 것과 동작이 동일합니다.'

classes_professor_post_responses = {
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
