from drf_yasg import openapi

class_enroll_operation_description = '기능\n' \
                                     '- 현재 로그인한 사용자가 수업 하나를 수강신청\n' \
                                     '\npermission\n' \
                                     '- admin 계정\n' \
                                     '- 로그인하고, 개인정보를 모두 세팅했고, 학생인 사용자\n' \
                                     '\nrequest body\n' \
                                     '- class_id(필수)\n' \
                                     '- user_id를 입력하지 않아도, 현재 token을 바탕으로 현재 요청을 넣는 사용자를 구분합니다.\n' \
                                     '\nresponses\n' \
                                     '- 201: 수강신청 성공'

class_enroll_request_body = openapi.Schema(
    'Enroll Class',
    type=openapi.TYPE_OBJECT,
    required=['class_id'],
    properties={
        'class_id': openapi.Schema(
            type=openapi.TYPE_INTEGER,
            description='수강신청할 수업의 id'
        ),
    },
)

class_enroll_responses = {
    201: openapi.Schema(
        'Success',
        type=openapi.TYPE_OBJECT,
        description='방금 전 수행한 수강신청을 반영한 현재 사용자의 수강하는 수업 리스트를 반환합니다.',
        properties={
            'classes': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    'Class',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            read_only=True,
                        ),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='수업 이름',
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
        },
    )
}
