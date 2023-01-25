from drf_yasg import openapi

announcement_get_operation_description = '기능\n' \
                                         '- 공지사항 하나의 정보를 자세히 가져옵니다.\n' \
                                         '- URL의 {id}에는 공지사항의 id가 들어갑니다.\n' \
                                         '\npermission\n' \
                                         '- admin 계정\n' \
                                         '- 로그인하고, 개인정보가 모두 세팅되어있는 사용자\n' \
                                         '\nrequest body\n' \
                                         '- 아무것도 담지 않습니다.\n' \
                                         '\nresponses\n' \
                                         '- 200: 공지사항 하나의 정보 가져오기 성공\n' \
                                         '\n비고\n' \
                                         '- created_at은 생성 시간으로, timestamp를 반환합니다.\n' \
                                         '- comments는 해당 공지사항에 달린 comment 리스트입니다.'

announcement_get_responses = {
    200: openapi.Schema(
        'Announcement Detail',
        type=openapi.TYPE_OBJECT,
        description='공지글의 세부정보입니다.',
        properties={
            'id': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                read_only=True,
            ),
            'title': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='공지글 제목입니다.',
            ),
            'content': openapi.Schema(
                type=openapi.TYPE_STRING,
                description='공지글 내용입니다. 특정 수업에 속한 공지글 리스트를 불러올 때와 다르게 문자열을 자르지 않고 모두 반환합니다.',
            ),
            'created_by': openapi.Schema(
                'User',
                type=openapi.TYPE_OBJECT,
                description='해당 공지글을 생성한 사람의 정보입니다.',
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
                description='timestamp 형식으로 공지글 생성 시간을 반환합니다.'
            ),
            'comment': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                description='해당 공지글에 달린 댓글 리스트입니다.',
                items=openapi.Schema(
                    'Comment',
                    type=openapi.TYPE_OBJECT,
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
                            description='timestamp 형식으로 댓글 생성 시간을 반환합니다.'
                        ),
                    }
                )
            ),
            'hits': openapi.Schema(
                type=openapi.TYPE_INTEGER,
                description='해당 공지글의 조회수입니다.\n"baseURL/etl/announcement/{id}/"에 GET 요청을 '
                            '넣을 때마다, 조회수는 1씩 증가합니다.'
            ),
        }
    )
}

announcement_patch_operation_description = '기능\n' \
                                         '- 공지사항 하나의 정보를 수정합니다.\n' \
                                         '- URL의 {id}에는 공지사항의 id가 들어갑니다.\n' \
                                         '\npermission\n' \
                                         '- admin 계정\n' \
                                         '- 로그인하고, 개인정보가 모두 세팅되어 있고, 해당 공지사항을 작성한 사용자\n' \
                                         '\nrequest body\n' \
                                         '- title(선택)\n' \
                                         '- content(선택)\n' \
                                         '\nresponses\n' \
                                         '- 200: PATCH 성공, 공지사항 하나의 정보 가져옴'

announcement_patch_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'title': openapi.Schema(
            type=openapi.TYPE_STRING,
        ),
        'content': openapi.Schema(
            type=openapi.TYPE_STRING,
        )
    },
    description='title이나 content를 수정합니다.'
)

announcement_patch_responses = announcement_get_responses

announcement_delete_operation_description = '기능\n' \
                                    '- 공지사항 하나 삭제\n' \
                                    '- {id}에 해당하는 게시글 하나를 삭제합니다.\n' \
                                    '\npermission\n' \
                                    '- admin 계정\n' \
                                    '- 로그인하고, 개인정보가 모두 세팅되어 있고, 해당 공지사항을 작성한 사용자\n' \
                                    '\nrequest body\n' \
                                    '- 아무것도 없습니다.\n' \
                                    '\nresponses\n' \
                                    '- 204: {id}에 해당하는 공지사항 하나 삭제 성공'
