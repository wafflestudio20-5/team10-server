from drf_yasg import openapi

comment_get_operation_description = '기능\n' \
                                    '- 특정 댓글의 정보를 가져옵니다.\n' \
                                    '- URL의 {id}에는 댓글의 id가 들어갑니다.\n' \
                                    '\npermission\n' \
                                    '- admin 계정\n' \
                                    '- 로그인하고, 개인정보 세팅을 완료한 사용자\n' \
                                    '\nrequest body\n' \
                                    '- 아무것도 없습니다.\n' \
                                    '\nresponses\n' \
                                    '- 200: 특정 댓글의 정보 가져오기 성공\n' \
                                    '\n비고\n' \
                                    '- Django에서 API 생성을 도와주는 라이브러리가 있어 생성하긴 하였으나, 당장은 GET 요청이 필요하지는 않을 것 같습니다.\n' \
                                    '본래 이런 API에서는 댓글 하나의 세부정보를 볼 수 있도록 지원해야 하나, etl/annuoncement/{id}/ 또는 ' \
                                    'etl/question/{id}/에서 comments에서 얻을 수 있는 정보보다 더 많은 것이 현재로서는 전혀 없습니다.\n' \
                                    '이 GET 요청을 받는 api는 당장은 아무 역할을 하지 않을 것으로 생각됩니다.'

comment_get_responses = {
    200: openapi.Schema(
        'Comment',
        type=openapi.TYPE_OBJECT,
        description='댓글 하나의 정보를 반환합니다.',
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                read_only=True,
            ),
            'content': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='댓글 내용입니다.',
            ),
            'created_by': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='해당 댓글을 생성한 사람의 정보입니다.',
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
                        description='유저가 교수인지, 학생인지 정보를 반환합니다.'
                    ),
                },
            ),
            'created_at': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='timestamp 형식으로 게시글 생성 시간을 반환합니다.'
            ),
        }
    )
}

# TODO: 다음 서버 배포 시 비고 삭제
comment_patch_operation_description = '기능\n' \
                                      '- 특정 댓글의 내용을 수정합니다.\n' \
                                      '- URL의 {id}는 댓글의 id를 의미합니다.\n' \
                                      '\npermission\n' \
                                      '- admin 계정\n' \
                                      '- 로그인 && 개인정보 세팅 완료 && (해당 댓글 작성자 || 교수자)\n' \
                                      '\nrequest body\n' \
                                      '- content(선택)\n' \
                                      '\nresponses\n' \
                                      '- 200: 특정 댓글 내용 수정 성공\n' \
                                      '\n비고\n' \
                                      '- permission을 잘못 설정했습니다. 현재 배포에서는 교수자가 댓글 내용을 수정할 수 없습니다. 다음 배포 때 고치겠습니다.'

comment_patch_request_body = openapi.Schema(
    'Comment',
    type=openapi.TYPE_OBJECT,
    properties={
        'content': openapi.Schema(
            type=openapi.TYPE_STRING,
            description='댓글 내용입니다.',
        ),
    }
)

comment_patch_responses = {
    200: openapi.Schema(
        'Comment',
        type=openapi.TYPE_OBJECT,
        description='방금 수정된 댓글 정보를 반환합니다.',
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                read_only=True,
            ),
            'content': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='댓글 내용입니다.',
            ),
            'created_by': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='해당 댓글을 생성한 사람의 정보입니다.',
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
                        description='유저가 교수인지, 학생인지 정보를 반환합니다.'
                    ),
                },
            ),
            'created_at': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='timestamp 형식으로 게시글 생성 시간을 반환합니다.'
            ),
        }
    )
}

# TODO: 다음 서버 배포 시 비고 삭제
comment_delete_operation_description = '기능\n' \
                                       '- 특정 댓글을 삭제합니다.\n' \
                                       '- URL의 {id}에는 삭제하고자 하는 댓글의 id가 들어갑니다.\n' \
                                       '\npermission\n' \
                                       '- admin 계정\n' \
                                       '- 로그인 && 개인정보 세팅 완료 && (해당 댓글 작성자 || 교수자)\n' \
                                       '\nrequest body\n' \
                                       '- 아무것도 없습니다.\n' \
                                       '\nresponses\n' \
                                       '- 204: 특정 댓글 삭제 성공\n' \
                                       '\n비고\n' \
                                       '- permission을 잘못 설정했습니다. 현재 배포에서는 교수자가 댓글을 삭제할 수 없습니다. 다음 배포 때 고치겠습니다.'
