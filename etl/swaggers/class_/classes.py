from drf_yasg import openapi

classes_get_operation_description = '기능\n' \
                                  '- 모든 존재하는 수업 목록을 불러옵니다.\n' \
                                  '- 페이지네이션이 적용되어, 이름 사전 순으로 수업을 10개씩 반환힙니다.\n' \
                                  '\n권한\n' \
                                  '- admin 계정\n' \
                                  '- 로그인한 사용자\n' \
                                  '\nrequest body\n' \
                                  '- 아무것도 없습니다.\n' \
                                  '\nresponses\n' \
                                  '- 200: 모든 수업 목록 받아오기 성공\n' \
                                  '\n사용 예시\n' \
                                  '- 세 번쩨 페이지에 해당하는 수업 목록을 불러오고 싶다면, "baseURL/etl/classes/?page=3"를 ' \
                                    '통해 가져올 수 있습니다.'

classes_get_responses = {
    200: openapi.Schema(
        'Class List',
        type=openapi.TYPE_OBJECT,
        properties={
            'count': openapi.Schema(
              type=openapi.TYPE_INTEGER,
              description='수업의 총 갯수를 반환합니다.'
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

classes_get_parameter_page = openapi.Parameter(
    'page',
    openapi.IN_QUERY,
    description='페이지네이션으로 해당하는 페이지를 반환합니다.',
    required=True,
    type=openapi.TYPE_INTEGER,
)

classes_get_manual_parameters = [classes_get_parameter_page]

classes_post_operation_description = '기능\n' \
                                   '- 수업 하나를 생성합니다.\n' \
                                   '\npermission\n' \
                                   '- admin 계정\n' \
                                   '- 로그인하고, 교수인 사용자\n' \
                                   '\nrequest body\n' \
                                   '- 수업 이름(필수)\n' \
                                   '\nresponses\n' \
                                   '- 201: 수업 하나 생성 성공, 생성한 수업 정보 반환.'

classes_post_request_body = openapi.Schema(
    'Class',
    type=openapi.TYPE_OBJECT,
    required=['name'],
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING)
    }
)

classes_post_responses = {
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
