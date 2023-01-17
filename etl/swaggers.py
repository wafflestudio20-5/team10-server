from drf_yasg import openapi


def get_enroll_drop_request_body(kind: str, description: str):
    return openapi.Schema(
        kind,
        type=openapi.TYPE_OBJECT,
        properties={
            'class_id': openapi.Schema('class id', type=openapi.TYPE_INTEGER),
        },
        description=description,
    )


def get_enroll_drop_responses(kind: str, description: str):
    return {
        201: openapi.Schema(
            kind,
            type=openapi.TYPE_OBJECT,
            properties={
                'classes': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        'Class',
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema('class id', read_only=True, type=openapi.TYPE_INTEGER),
                            'name': openapi.Schema('class name', type=openapi.TYPE_STRING),
                        }
                    )
                )
            },
            description=description
        )
    }


enroll_request_body = \
    get_enroll_drop_request_body('Enroll', '현재 로그인된 유저가 수강신청할 Class의 id를 request body에 '
                                           '담습니다. header에 담긴 토큰을 통해 현재 로그인된 유저를 확인합니다.')
enroll_responses = \
    get_enroll_drop_responses('Enroll', 'enroll 이후 현재 로그인된 유저가 수강하는 Class list를 반환합니다.')

drop_request_body = \
    get_enroll_drop_request_body('Drop', '현재 로그인된 유저가 드랍할 Class의 id를 request body에 담습니다. '
                                         'header에 담긴 토큰을 통해 현재 로그인된 유저를 확인합니다.')
drop_responses = \
    get_enroll_drop_responses('Drop', 'drop 이후 현재 로그인된 유저가 수강하는 Class list를 반환합니다.')

etl_class_get_operation_description = 'request body에 아무것도 담지 않습니다. 모든 존재하는 수업 목록을 불러옵니다. ' \
                                  '아직 pagination을 적용하지 않았습니다.'

etl_class_post_operation_description = 'request body에 만들 수업 이름을 담습니다. 수업은 교수만(is_professor = true)만' \
                                       ' 생성할 수 있도록 권한을 부여했습니다.'

etl_class_post_request_body = openapi.Schema(
    'Class',
    type=openapi.TYPE_OBJECT,
    properties={
        'name': openapi.Schema(type=openapi.TYPE_STRING)
    }
)

etl_class_professor_get_description = 'request body에 아무것도 담지 않습니다. header에 담긴 토큰을 통해' \
                                      ' 알아낸 현재 유저가 교수라면, 해당 유저가 생성한 수업 목록을 보여줍니다.' \
                                      ' 교수가 아니라면, 해당 API에 접근할 수 없도록 설정하였습니다.'

etl_class_professor_post_description = 'request body에 만들 수업 이름을 담습니다. 수업은 교수만(is_professor' \
                                       '=true) 생성할 수 있도록 권한을 부여했습니다. 사실 /etl/class/에' \
                                       ' POST 요청을 넣는 것과 하는 일이 동일합니다.'

etl_class_delete_operation_description = 'request body에 아무것도 담지 않습니다. URL에서 {id}는 수업의 id 값을' \
                                         ' 의미합니다. 해당 수업을 만든 본인이나, Admin 계정만이 수업을 삭제할 수 있도록' \
                                         ' 설정해두었습니다. 삭제가 잘 되었다면, response에서는 204 코드만을 반환합니다.'

etl_class_user_list_operation_descritpion = 'request body에 아무것도 담지 않습니다. URL에서 {id}는 수업의 id 값을 ' \
                                            '의미합니다. 페이지네이션을 적용해두었습니다. responses에서 next/previous는 이후/이전' \
                                            ' 유저의 목록을 불러옵니다. 페이지네이션 수 제한에 맞춘만큼의 유저 목록은 results에 담겨' \
                                            ' 보여집니다. 유저의 정보를 담고 있는 results 리스트에서 각 원소인 유저의 정보들은 ' \
                                            'etl에서 수강생 목록을 보여주는데 필요한 정보만을 담고 있습니다.'
