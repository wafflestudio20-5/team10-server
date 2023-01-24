from drf_yasg import openapi

classes_search_operation_description = "기능\n" \
                                       "- 수업 검색 기능을 지원합니다.\n" \
                                       "- 검색어를 URL에 parameter로 포함 시, 그에 맞는 수업 목록을 반환합니다.\n" \
                                       "- 페이지네이션이 적용되어, 이름 사전 순으로 수업을 10개씩 반환합니다.\n" \
                                       "\npermission\n" \
                                       "- admin 계정\n" \
                                       "- 로그인 && 개인정보 세팅 완료\n" \
                                       "\nrequest body\n" \
                                       "- 아무것도 없습니다.\n" \
                                       "\nparameters\n" \
                                       "- class_name(필수)\n" \
                                       "\nresponses\n" \
                                       "- 200: 수업 검색 성공\n" \
                                       "\n사용 예시\n" \
                                       "- '북' 키워드가 들어간 수업을 검색하고 싶을 때, 'baseURL/etl/classes/search/?class_name=북' 사용"

classes_search_responses = {
    200: openapi.Schema(
        'Class Search Result',
        type=openapi.TYPE_OBJECT,
        properties={
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
            )
        }
    )
}

classes_search_parameter_class_name = openapi.Parameter(
    'class_name',
    openapi.IN_QUERY,
    description='강의를 검색할 키워드를 담습니다.',
    required=True,
    type=openapi.TYPE_STRING,
)

classes_search_manual_parameters = [classes_search_parameter_class_name]

