from drf_yasg import openapi

user_get_operation_description = '기능\n' \
                                 '- 특정 유저의 정보 반환\n' \
                                 '- URL의 id에는 유저 id가 들어갑니다.\n' \
                                 '- 로그인으로 받은 토큰 정보를 토대로 유저의 정보를 받아오려면 이 API를 사용하시면 됩니다.\n' \
                                 '- 로그인 외에 그냥 유저 정보를 받아오고 싶으실 때도 활용하시면 됩니다.\n' \
                                 '\npermission\n' \
                                 '- admin 계정\n' \
                                 '- 로그인하고, 현재 자신의 정보를 조회하려는 사용자\n' \
                                 '(토큰이 나타내는 유저와 URL의 id가 나타내는 유저가 동일한지 확인)\n' \
                                 '\nrequest body\n' \
                                 '- 아무것도 없습니다.\n' \
                                 '\nresponses\n' \
                                 '- 200: 특정 유저 정보 가져오기 성공'

# TODO: properties 'profile' check
user_get_responses = {
    200: openapi.Schema(
        'User',
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(
                read_only=True,
                type=openapi.TYPE_INTEGER
            ),
            'email': openapi.Schema(
                type=openapi.TYPE_STRING
            ),
            'username': openapi.Schema(
                type=openapi.TYPE_STRING
            ),
            'student_id': openapi.Schema(
                type=openapi.TYPE_STRING
            ),
            'profile': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='유저의 사진이 담긴 url을 가져오는 것 같은데, 해당 기능을 담당하지 않아 확인이 필요합니다.'
            ),
            'is_professor': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description='사용자가 교수인지 정보를 반환합니다.'
            ),
            'is_superuser': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description='사용자가 admin인지 정보를 반환합니다.'
            ),
            'classes': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description='유저가 듣는 수업 목록을 리스트로 반환합니다.',
                items=openapi.Schema(
                    'Class',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            read_only=True,
                            type=openapi.TYPE_INTEGER
                        ),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='수업 이름입니다.'
                        ),
                    }
                )
            ),
        },
        description='특정 유저의 정보를 반환합니다.'
    ),
}

user_patch_operation_description = '기능\n' \
                                   '- 특정 유저의 정보 수정\n' \
                                   '- URL의 id에는 유저 id가 들어갑니다.\n' \
                                   '\npermission\n' \
                                   '- admin 계정\n' \
                                   '- 로그인했고, 현재 자신의 정보를 수정하려는 사용자' \
                                   '(토큰이 나타내는 유저와 URL의 id가 나타내는 유저가 동일한지 확인)\n' \
                                   '\nrequest body\n' \
                                   '- username(선택)\n' \
                                   '- student_id(선택)\n' \
                                   '\nresponses\n' \
                                   '- 200: 유저 정보 수정 성공 후, 수정이 반영된 유저 정보 반환.\n' \
                                   '\n비고\n' \
                                   '- student_id 조건 3개: 10글자, student_id[4]==\'-\', unique'

user_patch_request_body = openapi.Schema(
    'UserInfo Patch',
    type=openapi.TYPE_OBJECT,
    properties={
        'username': openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        'student_id': openapi.Schema(
            type=openapi.TYPE_STRING,
        )
    }
)

user_patch_responses = {
    200: openapi.Schema(
        'User',
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(
                read_only=True,
                type=openapi.TYPE_INTEGER
            ),
            'email': openapi.Schema(
                type=openapi.TYPE_STRING
            ),
            'username': openapi.Schema(
                type=openapi.TYPE_STRING
            ),
            'student_id': openapi.Schema(
                type=openapi.TYPE_STRING
            ),
            'profile': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='유저의 사진이 담긴 url을 가져오는 것 같은데, 해당 기능을 담당하지 않아 확인이 필요합니다.'
            ),
            'is_professor': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description='사용자가 교수인지 정보를 반환합니다.'
            ),
            'is_superuser': openapi.Schema(
                type=openapi.TYPE_BOOLEAN,
                description='사용자가 admin인지 정보를 반환합니다.'
            ),
            'classes': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description='유저가 듣는 수업 목록을 리스트로 반환합니다.',
                items=openapi.Schema(
                    'Class',
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(
                            read_only=True,
                            type=openapi.TYPE_INTEGER
                        ),
                        'name': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description='수업 이름입니다.'
                        ),
                    }
                )
            ),
        },
        description='특정 유저의 정보를 반환합니다.'
    ),
    400: openapi.Schema(
        'Fail',
        type=openapi.TYPE_OBJECT,
        properties={
            'student_id': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='1. 학번의 길이가 10글자가 아닐 때, "student_id should be 10 length" 메시지 반환\n'
                                '2. 5번째 글자가 "-"가 아닐 때, "student_id form should be XXXX-XXXXX" 메시지 반환\n'
                                '3. 이미 존재하는 학번일 때, "already existing student_id" 메시지 반환.\n'
                                '다만 수정 전 자신의 학번과 동일하게 PATCH 요청을 넣었을 때는, 오류를 반환하지 않습니다.\n'
                                '\n정규표현식으로 숫자 형식만이 입력되게는 제한을 걸어두지 않았습니다.'
                )
            )
        }
    )
}

user_delete_operation_description = '기능\n' \
                                       '- 특정 유저 삭제\n' \
                                       '- URL의 {id]는 삭제하려는 사용자의 id를 삽입\n' \
                                       '\n권한\n' \
                                       '- admin 계정\n' \
                                       '- 로그인하고, 현재 자신의 정보를 조회하려는 사용자\n' \
                                       '(토큰이 나타내는 유저와 URL의 id가 나타내는 유저가 동일한지 확인)\n' \
                                       '\nrequest body\n' \
                                       '- 없음\n' \
                                       '\nresponses\n' \
                                       '- 204: 특정 유저 삭제 성공'
