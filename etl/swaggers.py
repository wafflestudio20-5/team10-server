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
    get_enroll_drop_request_body('Enroll', '현재 로그인된 유저가 수강신청할 Class의 id를 입력')
enroll_responses = \
    get_enroll_drop_responses('Enroll', '수강신청 이후 현재 로그인된 유저가 수강하는 Class list를 반환')

drop_request_body = \
    get_enroll_drop_request_body('Drop', '현재 로그인된 유저가 드랍할 Class의 id를 입력')
drop_responses = \
    get_enroll_drop_responses('Drop', '드랍 이후 현재 로그인된 유저가 수강하는 Class list를 반환')
